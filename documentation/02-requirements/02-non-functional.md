# Non-Functional Requirements

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document defines the non-functional requirements (quality attributes) for PLACEHOLDER-PROJECT-NAME, specifying constraints on security, performance, reliability, usability, scalability, and maintainability. Each requirement includes specific, measurable targets.

---

## 1. Performance Requirements

| ID | Requirement | Target Metric |
|:---:|:---|:---|
| NF1.1 | API response time for `/api/analyze` (including model inference) | < 2 seconds for 95th percentile of requests |
| NF1.2 | CNN model inference latency per image | < 150 ms average (measured: Nail 93ms, Tongue 93ms, Skin 146ms) |
| NF1.3 | Frontend initial page load time (First Contentful Paint) | < 1.5 seconds on broadband connections |
| NF1.4 | Frontend Time to Interactive (TTI) | < 3 seconds on modern browsers |
| NF1.5 | Image preview rendering after file selection | < 100 ms (client-side `URL.createObjectURL`) |
| NF1.6 | Health check endpoint response time | < 50 ms (no model inference involved) |
| NF1.7 | Chart.js confidence chart rendering | < 200 ms after data availability |
| NF1.8 | Overpass API query response (Nearby Doctors) | < 5 seconds for 5 km radius queries |
| NF1.9 | Model loading time at server startup | < 5 seconds total for all 3 models |

---

## 2. Security Requirements

| ID | Requirement | Implementation |
|:---:|:---|:---|
| NF2.1 | Input validation: All uploaded files shall be validated for MIME type before processing | Backend validates `content_type` against `["image/jpeg", "image/png", "image/jpg"]`; rejects others with HTTP 400 |
| NF2.2 | Input sanitization: Body part parameter shall be validated against an allowlist | Backend checks `body_part` against `ALL_BODY_PARTS = ["Nail", "Skin", "Tongue"]` |
| NF2.3 | No persistent storage of user-uploaded images | Images are processed in-memory as NumPy arrays; no file system writes occur |
| NF2.4 | No collection or transmission of personally identifiable information (PII) | No user accounts, no authentication, no logging of user data |
| NF2.5 | CORS policy restricting cross-origin requests to known frontend origins | `CORS_ORIGINS` whitelist: `["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]` |
| NF2.6 | Location data privacy: Geolocation coordinates shall never be transmitted to the backend | Overpass API is called directly from the browser; backend has no access to user coordinates |
| NF2.7 | External links open in sandboxed contexts | All external links use `target="_blank"` with `rel="noopener noreferrer"` to prevent tabnapping |
| NF2.8 | No hardcoded secrets or API keys in the codebase | Configuration uses `pydantic-settings` with `.env` file support; no API keys required |

---

## 3. Reliability Requirements

| ID | Requirement | Implementation |
|:---:|:---|:---|
| NF3.1 | Graceful degradation when ML models are unavailable | `PredictorService` generates mock predictions via `numpy.random.dirichlet` when model files are missing; the UI explicitly labels these as mock results |
| NF3.2 | Error recovery for image decoding failures | `try/except` blocks in the analysis router catch OpenCV decode errors, returning structured HTTP 400 responses |
| NF3.3 | Network error handling on the frontend | Axios errors are caught and categorized: network errors, server validation errors, and generic failures — each with user-friendly messages |
| NF3.4 | Geolocation failure handling | Three failure modes handled: permission denied (specific re-enable instructions), timeout (generic retry), and unsupported browser (descriptive message) |
| NF3.5 | Overpass API failure resilience | HTTP errors from the Overpass API are caught; the UI displays "Failed to fetch nearby hospitals. Please try again." |
| NF3.6 | Race condition prevention in async operations | Nearby Doctors component uses a `cancelled` flag to prevent state updates from stale API responses after component unmount or radius change |
| NF3.7 | Server startup resilience | Model loading errors are caught in the FastAPI lifespan handler; the server starts in "demo mode" rather than crashing |

---

## 4. Usability Requirements

| ID | Requirement | Implementation |
|:---:|:---|:---|
| NF4.1 | Responsive layout across devices (320px – 2560px viewport widths) | CSS media queries with breakpoints; Grid/Flexbox layouts; mobile hamburger navigation |
| NF4.2 | Keyboard accessibility for all interactive elements | Dropzone supports `tabIndex={0}` and `onKeyDown` Enter handler; ARIA attributes on tabs, toggles, and navigation |
| NF4.3 | Screen reader support via semantic HTML and ARIA labels | Semantic elements (`<main>`, `<nav>`, `<header>`, `<article>`, `<section>`); `aria-label`, `aria-selected`, `aria-expanded`, `aria-hidden` attributes |
| NF4.4 | Browser compatibility | Supports latest 2 versions of Chrome, Firefox, Safari, and Edge (Vite's default browserslist) |
| NF4.5 | Visual loading indicators for all asynchronous operations | Spinner animations during analysis; skeleton loading states in ResultsPanel; map loading overlay |
| NF4.6 | Contextual help and guidance | Upload tips on each analysis page; step-by-step "How It Works" section; medical disclaimer |
| NF4.7 | Consistent visual theming | CSS custom properties for colors, spacing, typography; global dark/light mode toggle via `data-theme` attribute |
| NF4.8 | Intuitive drag-and-drop interface | Dropzone with visual feedback (border/background change on dragover); fallback click-to-browse; supported file types listed |

---

## 5. Scalability Requirements

| ID | Requirement | Implementation |
|:---:|:---|:---|
| NF5.1 | Horizontal model extensibility | Adding new body part analysis requires: (1) placing model in `backend/models/`, (2) adding config entries in `config.py`, (3) creating frontend page — no core architecture changes needed |
| NF5.2 | Diet plan extensibility | New deficiency food recommendations are added by extending the `FOOD_RECOMMENDATIONS` dictionary in `config.py` |
| NF5.3 | Concurrent request handling | FastAPI's async architecture supports multiple simultaneous requests; TensorFlow models are thread-safe for inference |
| NF5.4 | Memory-efficient model loading | Models are loaded once at startup (singleton pattern) and shared across all requests; estimated total RAM: ~750 MB for 3 models |
| NF5.5 | Frontend code splitting | Vite automatically performs tree-shaking and code splitting; React Router enables route-based lazy loading potential |

---

## 6. Maintainability Requirements

| ID | Requirement | Implementation |
|:---:|:---|:---|
| NF6.1 | Modular codebase organization | Backend: `models/`, `services/`, `routers/`, `utils/` packages; Frontend: `components/`, `pages/`, `services/`, `contexts/` directories |
| NF6.2 | Configuration externalization | All configurable values (model paths, CORS origins, image size) in `config.py` with environment variable overrides via `pydantic-settings` |
| NF6.3 | Type-safe API contracts | Pydantic schemas (`AnalysisResponse`, `HealthCheckResponse`, etc.) enforce request/response validation; FastAPI auto-generates OpenAPI documentation |
| NF6.4 | Code documentation standards | Python docstrings with Args/Returns blocks; JSDoc comments on exported functions; inline comments for non-obvious logic |
| NF6.5 | Development tooling | ESLint for JavaScript linting; Vite dev server with Hot Module Replacement; FastAPI `--reload` flag for auto-restart on code changes |
| NF6.6 | Version control | Git-based source control with `.gitignore` for `node_modules`, `__pycache__`, model files, and environment files |

---

## Requirements Summary

| Category | Count | Critical (Must Have) | Important | Nice to Have |
|:---|:---:|:---:|:---:|:---:|
| Performance | 9 | 4 | 3 | 2 |
| Security | 8 | 5 | 2 | 1 |
| Reliability | 7 | 4 | 3 | 0 |
| Usability | 8 | 4 | 3 | 1 |
| Scalability | 5 | 2 | 2 | 1 |
| Maintainability | 6 | 3 | 2 | 1 |
| **Total** | **43** | **22** | **15** | **6** |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
