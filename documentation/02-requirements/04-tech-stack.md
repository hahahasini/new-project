# Technology Stack

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document catalogs the complete technology stack used in PLACEHOLDER-PROJECT-NAME, including specific versions, usage within the project, and justification for each technology choice. The stack spans frontend, backend, machine learning, development tools, and external services.

---

## 1. Frontend Technologies

### 1.1 Core Framework

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **React** | 18.3.1 | UI component library | Industry-standard component-based library with virtual DOM for efficient re-rendering; functional components with hooks provide clean state management; massive ecosystem and community support |
| **React DOM** | 18.3.1 | DOM rendering | React's browser rendering package; v18 features concurrent rendering improvements |
| **Vite** | 5.4.0 | Build tool & dev server | Next-generation ES module-based build tool; near-instant Hot Module Replacement (HMR); significantly faster than webpack for development; native TypeScript support; optimized production builds with tree-shaking and code splitting |
| **@vitejs/plugin-react** | 4.3.1 | React integration for Vite | Provides Fast Refresh (hot reloading for React components) and JSX transformation |

### 1.2 Routing & State Management

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **React Router DOM** | 7.14.2 | Client-side routing | Declarative routing with nested layouts via `<Outlet />`; `NavLink` component for active-route styling; supports URL-based navigation without page reloads |
| **React Context API** | (built-in) | Global state management | Used for theme context (`ThemeProvider`/`useTheme`); lightweight alternative to Redux for simple global state; avoids external dependencies |

### 1.3 Data Visualization & Maps

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **Chart.js** | 4.4.4 | Charting library | Canvas-based charting with responsive design; supports bar charts for confidence score visualization; extensive customization via `options` API; performant rendering |
| **react-chartjs-2** | 5.2.0 | Chart.js React wrapper | Provides declarative React components (`<Bar />`) wrapping Chart.js; handles lifecycle management (mount/unmount/update) |
| **Leaflet** | 1.9.4 | Interactive maps | Lightweight, open-source mapping library; no API key required; supports custom markers, popups, and tile layers; 40KB gzipped |
| **react-leaflet** | 4.2.1 | Leaflet React wrapper | React component bindings for Leaflet (`<MapContainer>`, `<TileLayer>`, `<Marker>`, `<Popup>`); declarative map configuration |

### 1.4 HTTP Client

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **Axios** | 1.7.7 | HTTP client | Promise-based HTTP client with `multipart/form-data` support for image uploads; configurable timeouts (60s for model inference); interceptors for error handling; cleaner API than `fetch` for complex requests |

### 1.5 Development & Quality Tools

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **ESLint** | 9.8.0 | JavaScript linter | Catches common bugs and enforces code style; configured with React-specific plugins |
| **eslint-plugin-react** | 7.35.0 | React linting rules | React-specific lint rules (hooks rules, JSX accessibility) |
| **eslint-plugin-react-hooks** | 5.1.0-rc.0 | Hooks linting | Enforces Rules of Hooks (dependency arrays, call order) |
| **eslint-plugin-react-refresh** | 0.4.9 | Fast Refresh compatibility | Ensures components are compatible with Vite's fast refresh |

---

## 2. Backend Technologies

### 2.1 Web Framework

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **FastAPI** | 0.115.0 | REST API framework | High-performance async Python framework; automatic OpenAPI/Swagger documentation; native Pydantic integration for request/response validation; dependency injection system; lifespan events for startup/shutdown hooks; type hints throughout |
| **Uvicorn** | 0.30.0 (with `standard` extras) | ASGI server | Lightning-fast ASGI server for FastAPI; supports HTTP/1.1 and WebSocket; `--reload` flag for development auto-restart |

### 2.2 Configuration & Validation

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **Pydantic Settings** | 2.4.0 | Configuration management | Type-safe settings with environment variable overrides; `.env` file support; validation at startup; used for `Settings` class with `APP_NAME`, `APP_VERSION`, `CORS_ORIGINS`, model paths |
| **Pydantic** | (bundled with FastAPI) | Data validation | Schema definitions for all API models (`AnalysisResponse`, `HealthCheckResponse`, `PredictionScore`, `Meals`, `DietDay`, `DeficiencyDietPlan`); automatic JSON serialization; request body validation |
| **python-multipart** | 0.0.9 | Form data parsing | Required by FastAPI for `UploadFile` and `Form` parameter handling; parses `multipart/form-data` encoded image uploads |

### 2.3 Image Processing

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **OpenCV** (headless) | 4.10.0.84 | Image processing | Server-side image decoding (`imdecode`), color space conversion (`cvtColor BGR→RGB`), and spatial resizing (`resize` to 224×224); headless variant avoids unnecessary GUI dependencies on servers |
| **Pillow** | 10.4.0 | Image I/O fallback | Additional image format support; used as a dependency by other libraries |
| **NumPy** | 1.26.4 | Numerical computing | Array manipulation for image tensors; `frombuffer` for byte-to-array conversion; `expand_dims` for batch dimension; `argmax` for classification; `random.dirichlet` for mock predictions; float32 normalization |

---

## 3. Machine Learning Technologies

### 3.1 Framework & Models

| Technology | Version | Role | Justification |
|:---|:---:|:---|:---|
| **TensorFlow** | 2.16.1 | Deep learning framework | Industry-standard ML framework; Keras API for model definition and training; `.keras` format for model serialization; `model.predict()` for inference; `keras.models.load_model()` for weight loading; supports both CPU and GPU execution |
| **Keras** | (integrated in TF 2.16) | High-level neural network API | Simplified model architecture definition; built-in layers (Conv2D, Dense, MaxPool, BatchNorm, Dropout); training loop management; serialization via `.keras` format |

### 3.2 Model Architecture

| Model | Base Architecture | Training Approach | Epochs | Output Classes |
|:---|:---|:---|:---:|:---:|
| Nail CNN | MobileNetV2 / ResNet (transfer learning) | Fine-tuned on nail disease dataset | 24 | 3 (No Disease, Bluish nail, Alopecia areata) |
| Tongue CNN | MobileNetV2 / ResNet (transfer learning) | Fine-tuned on tongue disease dataset | 1 | 2 (Diabetes, Pale Tongue) |
| Skin CNN | MobileNetV2 / ResNet (transfer learning) | Fine-tuned on skin disease dataset | 46 | 2 (Acne, Carcinoma) |

### 3.3 Training Tools

| Technology | Role | Justification |
|:---|:---|:---|
| **Jupyter Notebooks** | Model training environment | Interactive development for data exploration, model training, and visualization; notebooks for Nail, Tongue, and Skin models |
| **Google Colab / Kaggle Notebooks** | Cloud compute | Free GPU/TPU access for model training; eliminates local GPU requirements |
| **Data Augmentation** (TF/Keras built-in) | Training data expansion | Rotations, horizontal flipping, zoom transformations to prevent overfitting and improve generalization |
| **Adam Optimizer** | Weight optimization | Adaptive learning rate optimizer; standard choice for CNN training |
| **Categorical Cross-Entropy** | Loss function | Standard loss for multi-class classification with softmax outputs |

### 3.4 Evaluation Tools

| Technology | Role | Justification |
|:---|:---|:---|
| **psutil** | Memory profiling | Measures process RSS (Resident Set Size) for RAM usage benchmarking during model loading |
| **Custom `benchmark_models.py`** | Performance profiling | Measures disk size, RAM delta, load time, and average inference latency across 10 iterations |
| **Custom `evaluate_accuracy.py`** | Accuracy evaluation | Iterates over held-out test datasets, computing per-class accuracy with folder-based ground truth matching |

---

## 4. External Services & APIs

| Service | Purpose | Protocol | Authentication |
|:---|:---|:---|:---|
| **Overpass API** (overpass-api.de) | Nearby hospital/clinic data | HTTP POST with OverpassQL query | None (public API) |
| **CartoDB Basemap** (basemaps.cartocdn.com) | Dark map tile layer | HTTPS tile URLs (`/{z}/{x}/{y}{r}.png`) | None (public tiles) |
| **Leaflet CDN** (cdnjs.cloudflare.com) | Default marker icons | HTTPS static assets | None |
| **Browser Geolocation API** | User location coordinates | `navigator.geolocation.getCurrentPosition` | Browser permission prompt |

---

## 5. Development Infrastructure

| Technology | Purpose | Justification |
|:---|:---|:---|
| **Git** | Version control | Distributed version control; `.gitignore` configured for `node_modules`, `__pycache__`, model files |
| **npm** | JavaScript package management | Standard Node.js package manager; `package-lock.json` for reproducible installs |
| **pip** | Python package management | Standard Python package manager; `requirements.txt` for reproducible installs |
| **Vite Dev Server** | Frontend development | ES module-based dev server with sub-second HMR; proxying not required (CORS configured) |
| **Uvicorn Dev Mode** | Backend development | `--reload` flag watches for file changes; automatic server restart on code modification |

---

## 6. Technology Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER'S BROWSER                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  React 18 + Vite 5                                  │    │
│  │  ├── React Router DOM 7 (SPA Routing)               │    │
│  │  ├── Axios 1.7 (HTTP Client)                        │    │
│  │  ├── Chart.js 4.4 + react-chartjs-2 (Charts)       │    │
│  │  ├── Leaflet 1.9 + react-leaflet (Maps)             │    │
│  │  ├── ThemeContext (Dark/Light Mode)                  │    │
│  │  └── Browser APIs (Geolocation, File, Drag & Drop)  │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │ HTTP (Axios)                        │
│                       ▼                                     │
│  ┌──────────────── Overpass API ────────────────────────┐   │
│  │  OpenStreetMap hospital/clinic queries               │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API (JSON + multipart/form-data)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND SERVER                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI 0.115 + Uvicorn 0.30 (ASGI)                │    │
│  │  ├── Pydantic Settings (Configuration)              │    │
│  │  ├── CORS Middleware (Origin Whitelist)              │    │
│  │  ├── Analysis Router (POST /api/analyze)            │    │
│  │  ├── Health Router (GET /api/health)                │    │
│  │  ├── PredictorService (TensorFlow 2.16 / Keras)     │    │
│  │  ├── DietPlannerService (Recommendation Engine)     │    │
│  │  ├── OpenCV 4.10 (Image Preprocessing)              │    │
│  │  └── NumPy 1.26 (Array Operations)                  │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼────────────────────────────────┐    │
│  │  ML Models (.keras files)                           │    │
│  │  ├── Nail_epoch_24.keras (273.64 MB)                │    │
│  │  ├── Tongue_epoch_01.keras (73.89 MB)               │    │
│  │  └── skin_disease_model_epoch_46.keras (84.24 MB)   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
