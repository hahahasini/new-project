# System Architecture

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

PLACEHOLDER-PROJECT-NAME follows a **decoupled client-server architecture** with a React single-page application (SPA) frontend communicating with a FastAPI REST backend. The backend serves as both an API gateway and an ML inference engine, loading three pre-trained TensorFlow/Keras CNN models at startup. The system is designed for local deployment, ensuring user privacy by processing all data in-memory without persistent storage.

See also: [Architecture Diagram](../diagrams/architecture.puml)

---

## 1. Major Components

### 1.1 Frontend Layer (React + Vite)
The frontend is a Single-Page Application built with React 18 and Vite 5, providing a rich, interactive user experience.

**Responsibilities**:
- Rendering the UI (home page, analysis pages, results panels)
- Managing client-side state (image selection, analysis results, theme, geolocation)
- Handling user interactions (drag-and-drop, form submission, tab switching)
- Communicating with the backend API via Axios HTTP client
- Directly querying the Overpass API for nearby doctors (browser-side)
- Rendering data visualizations (Chart.js bar charts, Leaflet maps)

**Key Sub-Components**:
| Component | Responsibility |
|:---|:---|
| `App.jsx` | Root router with nested layout (Navbar + Outlet + Footer) |
| `HomePage.jsx` | Hero section, model cards, stats, how-it-works, disclaimer |
| `NailPage / TonguePage / SkinPage` | Body-part-specific analysis pages with image upload and results |
| `ImageUploader.jsx` | Drag-and-drop image selection with preview |
| `ResultsPanel.jsx` | Orchestrates results display: summary, chart, diet, doctors |
| `ConfidenceChart.jsx` | Chart.js bar chart for per-class confidence scores |
| `DietPlan.jsx` | Tabbed weekly meal plans with download capability |
| `NearbyDoctors.jsx` | Geolocation → Overpass API → Leaflet map with doctor list |
| `Navbar.jsx` | Responsive navigation with theme toggle and mobile menu |
| `ThemeContext.jsx` | Global dark/light mode state via React Context API |
| `api.js` | Axios-based API client for backend communication |

### 1.2 Backend Layer (FastAPI + Uvicorn)
The backend provides a high-performance REST API that handles image analysis requests, model inference, and diet plan generation.

**Responsibilities**:
- Accepting and validating image uploads (MIME type, body part)
- Preprocessing images for model consumption (decode, resize, normalize)
- Executing CNN model inference via TensorFlow
- Generating diet recommendations based on prediction results
- Serving health check information
- Managing model lifecycle (load at startup, shared across requests)

**Key Sub-Components**:
| Module | Responsibility |
|:---|:---|
| `main.py` | FastAPI app initialization, CORS config, lifespan management, router mounting |
| `config.py` | Settings (Pydantic), domain data (classes, diseases, food recommendations) |
| `analysis.py` (router) | Endpoint handlers for `/api/analyze` and `/api/health` |
| `predictor.py` (service) | Model loading, image preprocessing, CNN inference, result mapping |
| `diet_planner.py` (service) | Weekly meal plan generation with cyclic food assignment |
| `image_processing.py` (utils) | Image decode, resize, normalize, and preprocess utilities |
| `schemas.py` (models) | Pydantic models for request/response validation |

### 1.3 ML Model Layer (TensorFlow/Keras)
Three custom-trained CNN models handle body-part-specific image classification.

| Model | File | Disk Size | RAM | Classes |
|:---|:---|:---:|:---:|:---:|
| Nail CNN | `nail/Nail_epoch_24.keras` | 273.64 MB | 578.79 MB | 3 |
| Tongue CNN | `tongue/Tongue_epoch_01.keras` | 73.89 MB | 92.36 MB | 2 |
| Skin CNN | `skin/skin_disease_model_epoch_46.keras` | 84.24 MB | 77.89 MB | 2 |

### 1.4 External Services
| Service | Role | Protocol |
|:---|:---|:---|
| Overpass API | Hospital/clinic geospatial queries | HTTP POST (OverpassQL) |
| CartoDB Tiles | Map tile rendering | HTTPS GET (z/x/y tiles) |
| Browser Geolocation | User location coordinates | JavaScript API |
| Leaflet CDN | Map marker icon assets | HTTPS GET |

---

## 2. Data Flow

```
User → [Select body part] → [Upload image] → [Click Analyze]
         │
         ▼
Frontend: Create FormData(file, body_part)
         │
         ▼ HTTP POST /api/analyze (multipart/form-data)
         │
Backend:  Validate inputs → Decode image → Preprocess (224×224, normalize)
         │
         ▼ model.predict(img_array)
         │
ML Model: Forward pass → Softmax probabilities → [0.12, 0.05, 0.83]
         │
         ▼ argmax → class index → map to labels
         │
Backend:  deficiency="Vitamin D", disease="Alopecia areata", confidence=83%
         │ + Generate diet plans for all classes
         │
         ▼ JSON response (AnalysisResponse)
         │
Frontend: Render ResultsPanel → Chart → DietPlan → NearbyDoctors
```

---

## 3. Communication Protocols

| Channel | Protocol | Format | Auth |
|:---|:---|:---|:---|
| Frontend ↔ Backend | HTTP/1.1 REST | JSON + multipart/form-data | None (local) |
| Frontend ↔ Overpass API | HTTP/1.1 POST | URL-encoded OverpassQL | None (public) |
| Frontend ↔ CartoDB | HTTPS GET | PNG tile images | None (public) |
| Frontend ↔ Geolocation | JavaScript API | Position object | Browser permission |

---

## 4. Architectural Patterns

### 4.1 Service-Oriented Backend
The backend follows a **service-oriented architecture** with clear separation:
- **Routers** handle HTTP concerns (request parsing, response formatting, error codes)
- **Services** contain business logic (prediction, diet planning) as class-level methods
- **Utils** provide reusable image processing functions
- **Models** define data contracts (Pydantic schemas)

### 4.2 Component-Based Frontend
The frontend follows **React's component composition pattern**:
- **Pages** compose **Components** to build full-page layouts
- **Components** are single-responsibility, reusable units
- **Services** abstract external communication (API calls)
- **Contexts** provide global state (theme) without prop drilling

### 4.3 Singleton Model Management
ML models are loaded once at startup using FastAPI's `asynccontextmanager` lifespan events:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    PredictorService.load_models()  # Load once
    yield                            # Serve requests
    # Cleanup on shutdown
```
Models are stored as class-level attributes in `PredictorService._models`, shared across all incoming requests without reloading.

---

## 5. Scalability Approach

| Dimension | Strategy |
|:---|:---|
| **Model Extensibility** | Add new body parts by: placing model file → adding config entries → creating frontend page |
| **Horizontal Scaling** | Deploy multiple Uvicorn workers behind a reverse proxy (Nginx) for concurrent request handling |
| **Model Offloading** | For GPU acceleration, TensorFlow can use CUDA-enabled GPUs without code changes |
| **Static Frontend** | Vite build produces static assets deployable to any CDN or static hosting service |
| **API Gateway** | FastAPI supports middleware for rate limiting, authentication, and request logging |

---

## 6. Failure Handling & Resilience

| Failure Scenario | Handling Strategy |
|:---|:---|
| Model file missing | Mock predictions via Dirichlet distribution; UI shows "Mock Prediction" warning |
| Image decoding failure | Caught exception → HTTP 400 with descriptive error message |
| Invalid body part | Allowlist validation → HTTP 400 with valid options listed |
| Network error (frontend) | Axios catch → user-friendly error message with retry guidance |
| Overpass API down | Caught fetch error → "Failed to fetch nearby hospitals" with retry option |
| Location denied | State machine transitions to "denied" state → retry button available |
| TensorFlow crash | Exception caught in lifespan → server starts in demo mode |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
