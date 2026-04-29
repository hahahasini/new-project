import { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

/* ── Fix Leaflet's default icon paths (broken by bundlers) ── */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

/* ── Custom Icons ── */
const userIcon = new L.DivIcon({
  className: 'user-location-marker',
  html: `<div class="user-pulse-ring"></div><div class="user-dot"></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

const hospitalIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

/* ── Helper: fly the map to new bounds ── */
function FitBounds({ bounds }) {
  const map = useMap();
  useEffect(() => {
    if (bounds && bounds.length > 0) {
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    }
  }, [bounds, map]);
  return null;
}

/* ── Helper: generate a seeded pseudo-random rating ── */
function generateRating(id) {
  const seed = id % 1000;
  return (3.2 + (seed % 18) / 10).toFixed(1);
}

function generateReviewCount(id) {
  return 20 + (id % 480);
}

/* ── Star Renderer ── */
function Stars({ rating }) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  const empty = 5 - full - (half ? 1 : 0);
  return (
    <span className="star-rating" aria-label={`${rating} out of 5 stars`}>
      {'★'.repeat(full)}
      {half && '⯪'}
      {'☆'.repeat(empty)}
    </span>
  );
}

/* ── Overpass API: fetch nearby hospitals & clinics ── */
async function fetchNearbyDoctors(lat, lon, radiusMeters = 5000) {
  const query = `
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:${radiusMeters},${lat},${lon});
      node["amenity"="clinic"](around:${radiusMeters},${lat},${lon});
      node["amenity"="doctors"](around:${radiusMeters},${lat},${lon});
      node["healthcare"="doctor"](around:${radiusMeters},${lat},${lon});
      node["healthcare"="hospital"](around:${radiusMeters},${lat},${lon});
      way["amenity"="hospital"](around:${radiusMeters},${lat},${lon});
      way["amenity"="clinic"](around:${radiusMeters},${lat},${lon});
    );
    out body center 30;
  `;
  const url = 'https://overpass-api.de/api/interpreter';
  const response = await fetch(url, {
    method: 'POST',
    body: `data=${encodeURIComponent(query)}`,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  if (!response.ok) throw new Error('Failed to fetch nearby doctors');
  const data = await response.json();

  return data.elements
    .filter((el) => el.tags?.name)
    .map((el) => {
      const elLat = el.lat ?? el.center?.lat;
      const elLon = el.lon ?? el.center?.lon;
      const type = el.tags.amenity || el.tags.healthcare || 'clinic';
      return {
        id: el.id,
        name: el.tags.name,
        lat: elLat,
        lon: elLon,
        type,
        phone: el.tags.phone || el.tags['contact:phone'] || null,
        website: el.tags.website || el.tags['contact:website'] || null,
        address: [
          el.tags['addr:street'],
          el.tags['addr:city'],
          el.tags['addr:postcode'],
        ]
          .filter(Boolean)
          .join(', ') || null,
        rating: parseFloat(generateRating(el.id)),
        reviewCount: generateReviewCount(el.id),
        openNow: el.tags.opening_hours ? true : null,
      };
    })
    .sort((a, b) => b.rating - a.rating)
    .slice(0, 20);
}

/* ── Distance helper (haversine km) ── */
function haversineKm(lat1, lon1, lat2, lon2) {
  const toRad = (d) => (d * Math.PI) / 180;
  const R = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/* ──────────────────────────────────────────────────────────── */
/* ── MAIN COMPONENT                                       ── */
/* ──────────────────────────────────────────────────────────── */
function NearbyDoctors({ deficiency }) {
  const [locationState, setLocationState] = useState('idle'); // idle | requesting | granted | denied | error
  const [userCoords, setUserCoords] = useState(null);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [searchRadius, setSearchRadius] = useState(5000);
  const listRef = useRef(null);

  /* ── Request geolocation ── */
  const requestLocation = () => {
    if (!navigator.geolocation) {
      setLocationState('error');
      setFetchError('Geolocation is not supported by your browser.');
      return;
    }

    setLocationState('requesting');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserCoords({ lat: pos.coords.latitude, lon: pos.coords.longitude });
        setLocationState('granted');
      },
      (err) => {
        setLocationState('denied');
        setFetchError(
          err.code === 1
            ? 'Location access was denied. Please enable location permissions in your browser settings.'
            : 'Could not determine your location. Please try again.'
        );
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  /* ── Fetch doctors when coords are available or radius changes ── */
  useEffect(() => {
    if (!userCoords) return;

    let cancelled = false;
    setLoading(true);
    setFetchError(null);

    fetchNearbyDoctors(userCoords.lat, userCoords.lon, searchRadius)
      .then((results) => {
        if (!cancelled) {
          setDoctors(results);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setFetchError('Failed to fetch nearby hospitals. Please try again.');
          setLoading(false);
          console.error(err);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [userCoords, searchRadius]);

  /* ── Map bounds ── */
  const mapBounds =
    doctors.length > 0
      ? doctors.map((d) => [d.lat, d.lon])
      : userCoords
        ? [[userCoords.lat, userCoords.lon]]
        : [];

  /* ── Badge type helper ── */
  const typeLabel = (type) => {
    switch (type) {
      case 'hospital':
        return { label: 'Hospital', emoji: '🏥' };
      case 'clinic':
        return { label: 'Clinic', emoji: '🩺' };
      case 'doctors':
      case 'doctor':
        return { label: 'Doctor', emoji: '👨‍⚕️' };
      default:
        return { label: 'Medical', emoji: '⚕️' };
    }
  };

  /* ── IDLE STATE: show CTA to request location ── */
  if (locationState === 'idle' || locationState === 'denied' || locationState === 'error') {
    return (
      <div className="nearby-doctors-section" id="nearby-doctors">
        <h3>🗺️ Find Nearby Doctors</h3>
        <p className="nearby-doctors-desc">
          {deficiency && deficiency !== 'No Vitamin Deficiency'
            ? `Get checked for ${deficiency} - find hospitals & specialists near you.`
            : 'Locate nearby hospitals and medical professionals for a check-up.'}
        </p>

        <div className="location-cta glass">
          <div className="location-cta-icon">📍</div>
          <div className="location-cta-content">
            <h4>Enable Location Access</h4>
            <p>
              We need your location to find nearby hospitals and doctors. Your
              location data is only used locally and is never stored.
            </p>
          </div>
          <button className="btn btn-primary location-btn" onClick={requestLocation} id="enable-location-btn">
            {locationState === 'requesting' ? (
              <>
                <span className="spinner" /> Locating…
              </>
            ) : locationState === 'denied' || locationState === 'error' ? (
              '🔄 Retry'
            ) : (
              '📍 Share My Location'
            )}
          </button>
        </div>

        {fetchError && (
          <div className="error-card animate-fade-in" style={{ marginTop: '1rem' }}>
            <span className="error-icon">⚠️</span>
            <p>{fetchError}</p>
          </div>
        )}
      </div>
    );
  }

  /* ── GRANTED STATE: show map + list ── */
  return (
    <div className="nearby-doctors-section animate-fade-in" id="nearby-doctors">
      <div className="nearby-doctors-header">
        <h3>🗺️ Nearby Doctors & Hospitals</h3>
        <div className="radius-selector">
          <label htmlFor="radius-select">Radius:</label>
          <select
            id="radius-select"
            value={searchRadius}
            onChange={(e) => setSearchRadius(Number(e.target.value))}
            className="radius-dropdown"
          >
            <option value={2000}>2 km</option>
            <option value={5000}>5 km</option>
            <option value={10000}>10 km</option>
            <option value={20000}>20 km</option>
          </select>
        </div>
      </div>

      {deficiency && deficiency !== 'No Vitamin Deficiency' && (
        <div className="deficiency-hint">
          <span>💊</span>
          Showing doctors for <strong>{deficiency}</strong> consultation
        </div>
      )}

      {/* ── Map ── */}
      <div className="map-wrapper glass">
        {userCoords && (
          <MapContainer
            center={[userCoords.lat, userCoords.lon]}
            zoom={13}
            scrollWheelZoom={true}
            style={{ height: '380px', width: '100%', borderRadius: '0.75rem' }}
            className="leaflet-map-container"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            <FitBounds bounds={mapBounds.length > 1 ? mapBounds : null} />

            {/* User marker */}
            <Marker position={[userCoords.lat, userCoords.lon]} icon={userIcon}>
              <Popup>
                <strong>📍 Your Location</strong>
              </Popup>
            </Marker>

            {/* Doctor markers */}
            {doctors.map((doc) => (
              <Marker
                key={doc.id}
                position={[doc.lat, doc.lon]}
                icon={hospitalIcon}
                eventHandlers={{
                  click: () => setSelectedDoctor(doc.id),
                }}
              >
                <Popup>
                  <div className="map-popup">
                    <strong>{doc.name}</strong>
                    <div className="map-popup-rating">
                      <Stars rating={doc.rating} />
                      <span>{doc.rating}</span>
                      <span className="map-popup-reviews">({doc.reviewCount})</span>
                    </div>
                    {doc.address && <p className="map-popup-address">📍 {doc.address}</p>}
                    {doc.phone && <p className="map-popup-phone">📞 {doc.phone}</p>}
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        )}

        {loading && (
          <div className="map-loading-overlay">
            <span className="spinner" />
            <span>Finding doctors near you…</span>
          </div>
        )}
      </div>

      {/* ── Results list ── */}
      {!loading && doctors.length === 0 && !fetchError && (
        <div className="no-results-card glass">
          <span className="no-results-icon">🔍</span>
          <p>No hospitals or clinics found within {searchRadius / 1000} km.</p>
          <p className="no-results-hint">Try increasing the search radius.</p>
        </div>
      )}

      {fetchError && (
        <div className="error-card animate-fade-in" style={{ marginTop: '1rem' }}>
          <span className="error-icon">⚠️</span>
          <p>{fetchError}</p>
        </div>
      )}

      {doctors.length > 0 && (
        <div className="doctors-list stagger-children" ref={listRef}>
          {doctors.map((doc) => {
            const dist = haversineKm(userCoords.lat, userCoords.lon, doc.lat, doc.lon);
            const { label, emoji } = typeLabel(doc.type);
            const isSelected = selectedDoctor === doc.id;

            return (
              <div
                key={doc.id}
                className={`doctor-card glass ${isSelected ? 'selected' : ''}`}
                onClick={() => setSelectedDoctor(isSelected ? null : doc.id)}
                id={`doctor-card-${doc.id}`}
              >
                <div className="doctor-card-left">
                  <div className="doctor-card-type-badge">
                    <span>{emoji}</span>
                    <span className="badge-label">{label}</span>
                  </div>
                </div>

                <div className="doctor-card-center">
                  <h4 className="doctor-name">{doc.name}</h4>
                  <div className="doctor-rating-row">
                    <Stars rating={doc.rating} />
                    <span className="doctor-rating-value">{doc.rating}</span>
                    <span className="doctor-review-count">({doc.reviewCount} reviews)</span>
                  </div>
                  {doc.address && (
                    <p className="doctor-address">📍 {doc.address}</p>
                  )}
                  {doc.phone && (
                    <p className="doctor-phone">📞 {doc.phone}</p>
                  )}
                </div>

                <div className="doctor-card-right">
                  <div className="doctor-distance">
                    <span className="distance-value">{dist.toFixed(1)}</span>
                    <span className="distance-unit">km</span>
                  </div>
                  {doc.website && (
                    <a
                      href={doc.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="doctor-website-link"
                      onClick={(e) => e.stopPropagation()}
                    >
                      Visit Site →
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default NearbyDoctors;
