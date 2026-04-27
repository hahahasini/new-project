import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import ImageUploader from './components/ImageUploader';
import BodyPartSelector from './components/BodyPartSelector';
import ResultsPanel from './components/ResultsPanel';
import Footer from './components/Footer';
import { analyzeImage } from './services/api';

const BODY_PARTS = [
  { id: 'Nail', label: 'Nail', icon: '💅', hasModel: true },
  { id: 'Tongue', label: 'Tongue', icon: '👅', hasModel: true },
  { id: 'Skin', label: 'Skin', icon: '🧴', hasModel: true },
];

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [selectedBodyPart, setSelectedBodyPart] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResults(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage || !selectedBodyPart) return;

    setLoading(true);
    setError(null);

    try {
      const data = await analyzeImage(selectedImage, selectedBodyPart);
      setResults(data);
    } catch (err) {
      console.error('Analysis failed:', err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.message.includes('Network Error')) {
        setError('Cannot connect to the server. Please make sure the backend is running on port 8000.');
      } else {
        setError('Analysis failed. Please try again with a different image.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setSelectedBodyPart(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <div className="container">
          {/* Hero Section */}
          <section className="hero-section animate-fade-in-up">
            <h1 className="hero-title">
              <span className="gradient-text">Vitamin Deficiency</span>
              <br />
              Detection System
            </h1>
            <p className="hero-subtitle">
              Upload an image of your <strong>nail</strong>, <strong>skin</strong>, or{' '}
              <strong>tongue</strong> to detect potential vitamin
              deficiencies using AI-powered image analysis.
            </p>
          </section>

          {/* Upload + Results Layout */}
          <div className={`analysis-layout ${(!results && !loading) ? 'centered' : ''}`}>
            <div className="upload-section animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              <ImageUploader
                onImageSelect={handleImageSelect}
                previewUrl={previewUrl}
                onAnalyze={handleAnalyze}
                onReset={handleReset}
                loading={loading}
                hasImage={!!selectedImage}
                canAnalyze={!!selectedBodyPart}
              />

              {/* Body Part Selector — shown after image is uploaded */}
              {selectedImage && !results && !loading && (
                <BodyPartSelector
                  bodyParts={BODY_PARTS}
                  selected={selectedBodyPart}
                  onSelect={setSelectedBodyPart}
                />
              )}

              {error && (
                <div className="error-card animate-fade-in">
                  <span className="error-icon">⚠️</span>
                  <p>{error}</p>
                </div>
              )}
            </div>

            {(results || loading) && (
              <div className="results-section animate-slide-in-right">
                <ResultsPanel results={results} loading={loading} />
              </div>
            )}
          </div>

          {/* Feature Cards */}
          {!results && !loading && (
            <section className="features-section stagger-children">
              <div className="feature-card glass">
                <div className="feature-icon">💅</div>
                <h3>Nail Analysis</h3>
                <p>Identify Iodine and Vitamin D deficiencies from nail conditions</p>
                <span className="feature-badge available">Model Available</span>
              </div>
              <div className="feature-card glass">
                <div className="feature-icon">👅</div>
                <h3>Tongue Analysis</h3>
                <p>Spot Vitamin B12 and Iron deficiencies from tongue appearance</p>
                <span className="feature-badge available">Model Available</span>
              </div>

              <div className="feature-card glass">
                <div className="feature-icon">🧴</div>
                <h3>Skin Analysis</h3>
                <p>Recognize Vitamin A and D deficiencies from skin conditions</p>
                <span className="feature-badge available">Model Available</span>
              </div>
            </section>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
