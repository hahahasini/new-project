# Program Specific Outcome (PSO) Mapping

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection Using Image Processing and Deep Learning  
> **Institution**: PLACEHOLDER-INSTITUTION | **Year**: PLACEHOLDER-YEAR | **Semester**: PLACEHOLDER-SEMESTER  
> **Team**: PLACEHOLDER-TEAM-MEMBER-1, PLACEHOLDER-TEAM-MEMBER-2, PLACEHOLDER-TEAM-MEMBER-3, PLACEHOLDER-TEAM-MEMBER-4  
> **Faculty Guide**: PLACEHOLDER-FACULTY (PLACEHOLDER-FACULTY-ROLE)

---

## Overview

Program Specific Outcomes (PSOs) are discipline-specific competencies that graduates of a PLACEHOLDER-BRANCH program are expected to demonstrate. This document maps PLACEHOLDER-PROJECT-NAME to 6 PSOs, demonstrating how the project develops competencies in software development, machine learning, data engineering, and systems integration.

---

## P-PSO Mapping Table

| Project Code | PSO | Level | Justification |
|:---:|:---|:---:|:---|
| PLACEHOLDER-PROJECT-NAME | **PSO1: Software Development Competency** — Ability to design, develop, test, and deploy software systems using modern programming languages, frameworks, and development methodologies. | **H** | The backend is built with **FastAPI** (Python 3.9+), using `APIRouter` for route organization, Pydantic schemas for validation (`AnalysisResponse`, `HealthCheckResponse`, `PredictionScore`, `Meals`, `DietDay`, `DeficiencyDietPlan`), CORS middleware for cross-origin access control, and `asynccontextmanager` for startup model loading. The frontend is a **React 18** SPA using Vite, with functional components and hooks (`useState`, `useEffect`, `useRef`), Context API for theme state (`ThemeProvider`/`useTheme`), `react-router-dom` v7 for nested routing with `<Outlet />`, and Axios for HTTP calls. The codebase follows separation of concerns — services (`predictor.py`, `diet_planner.py`, `api.js`), models (`schemas.py`), routers (`analysis.py`), utils (`image_processing.py`), components, pages, and contexts are in dedicated modules. |
| PLACEHOLDER-PROJECT-NAME | **PSO2: Machine Learning & AI Competency** — Ability to apply machine learning algorithms, neural network architectures, and data-driven techniques to solve real-world problems. | **H** | Three CNN models are trained using transfer learning (MobileNetV2/ResNet base architectures) and fine-tuned for medical image classification. Training was performed in Jupyter notebooks (`nail disease.ipynb`, `skin disease.ipynb`, `tongue.ipynb`). Models are serialized as `.keras` files, loaded at server startup, and execute predictions on preprocessed 224×224 RGB images normalized to [0,1] float32. A dedicated `evaluate_accuracy.py` script measures per-class accuracy against held-out test sets (Nail: 134 samples/3 classes, Tongue: 76 samples/2 classes, Skin: 280 samples/2 classes). A `benchmark_models.py` script measures inference latency (92–146ms average), RAM usage (77–579 MB), and load time. The Skin model achieves 98.57% accuracy on Acne and 97.14% on Carcinoma. |
| PLACEHOLDER-PROJECT-NAME | **PSO3: Data Engineering & Management** — Ability to design data models, manage data pipelines, and implement efficient data storage and retrieval mechanisms. | **M** | The project uses a configuration-driven data architecture in `config.py`: `CLASSES` maps body parts to deficiency labels, `DISEASES` maps to disease labels (index-aligned with model outputs), and `FOOD_RECOMMENDATIONS` contains a 14-category food database with structured breakfast/lunch/dinner arrays. The image processing pipeline implements: raw bytes → `np.frombuffer` → `cv2.imdecode` → `cv2.cvtColor(BGR→RGB)` → `cv2.resize(224×224)` → `float32/255.0` → `np.expand_dims` batch axis. Pydantic schemas enforce type safety on all API responses. The `DietPlannerService` uses cyclic indexing (`foods["breakfast"][i % len(foods["breakfast"])]`) to map 3-4 food options to 7-day plans. |
| PLACEHOLDER-PROJECT-NAME | **PSO4: Systems Integration & API Design** — Ability to integrate heterogeneous systems, design RESTful APIs, and implement inter-service communication protocols. | **H** | The project integrates five distinct technology layers: (1) **React ↔ FastAPI** — multipart/form-data image upload and JSON response parsing via Axios; (2) **FastAPI ↔ TensorFlow** — `PredictorService` abstracts model loading and inference behind a class-level API; (3) **React ↔ OpenStreetMap** — the `NearbyDoctors` component queries the Overpass API directly from the browser using OverpassQL to fetch hospital/clinic data; (4) **React ↔ Browser APIs** — Geolocation API for coordinates (`navigator.geolocation.getCurrentPosition`) and File API for drag-and-drop image handling; (5) **React ↔ Chart.js** — prediction scores piped into `react-chartjs-2` for bar chart rendering. The REST API uses proper HTTP status codes (200, 400, 422), content-type validation, and structured error responses. |
| PLACEHOLDER-PROJECT-NAME | **PSO5: User Interface & Experience Design** — Ability to design and implement user-centered interfaces that are accessible, responsive, and aesthetically refined. | **H** | The frontend implements: (1) **Responsive design** — CSS custom properties for colors/spacing/typography, media queries for breakpoints, CSS Grid for model cards, Flexbox for layouts; (2) **Theme system** — dark/light mode via `[data-theme]` CSS selectors and React Context; (3) **Accessibility** — ARIA attributes (`aria-label`, `aria-selected`, `aria-expanded`), semantic HTML (`<main>`, `<nav>`, `<article>`, `<section>`), keyboard navigation (`tabIndex`, `onKeyDown` on dropzone), and role attributes (`role="tablist"`, `role="tab"`); (4) **Animations** — CSS keyframes (`animate-fade-in`, `animate-fade-in-up`, `animate-slide-in-right`, `stagger-children`), skeleton loading states, glassmorphism effects (`.glass` class), and confidence-colored indicators; (5) **Components** — 9 reusable components (`ImageUploader`, `ConfidenceChart`, `DietPlan`, `NearbyDoctors`, `ResultsPanel`, `Navbar`, `Footer`, `Header`, `BodyPartSelector`). |
| PLACEHOLDER-PROJECT-NAME | **PSO6: Problem Domain Knowledge** — Ability to acquire and apply domain-specific knowledge relevant to the problem being solved. | **M** | The project encodes nutritional domain knowledge in its configuration: nail conditions (bluish nails → iodine deficiency, alopecia areata → vitamin D deficiency), tongue indicators (pale tongue → iron deficiency, diabetes → vitamin B12 deficiency), and skin conditions (acne → vitamin D deficiency, carcinoma → vitamin A deficiency). The `FOOD_RECOMMENDATIONS` dictionary in `config.py` maps 14 deficiency categories to targeted dietary recommendations. The `models.md` document proposes five additional detection modules (Hair, Lips, Gums, Facial Pallor, Retina) with justifications for which deficiencies each would detect. The medical disclaimer and confidence-based reporting demonstrate awareness of responsible deployment of medical AI tools. |

---

## PSO Summary

| PSO | Level | Key Evidence |
|:---:|:---:|:---|
| PSO1 | H | FastAPI, React 18, Vite, Pydantic, React Router, Hooks, Context API |
| PSO2 | H | TensorFlow/Keras CNNs, Transfer Learning, Evaluation Scripts, Benchmark Scripts |
| PSO3 | M | Config-driven data model, Image processing pipeline, Pydantic schemas |
| PSO4 | H | REST API, Multipart upload, Overpass API, Geolocation API, Chart.js |
| PSO5 | H | CSS design system, Themes, ARIA accessibility, Animations, 9 components |
| PSO6 | M | Nutritional deficiency mappings, 14-category food database, Future model proposals |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
