# Program Outcome (PO) Mapping

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection Using Image Processing and Deep Learning  
> **Institution**: PLACEHOLDER-INSTITUTION | **Year**: PLACEHOLDER-YEAR | **Semester**: PLACEHOLDER-SEMESTER  
> **Team**: PLACEHOLDER-TEAM-MEMBER-1, PLACEHOLDER-TEAM-MEMBER-2, PLACEHOLDER-TEAM-MEMBER-3, PLACEHOLDER-TEAM-MEMBER-4  
> **Faculty Guide**: PLACEHOLDER-FACULTY (PLACEHOLDER-FACULTY-ROLE)

---

## Overview

This document maps the PLACEHOLDER-PROJECT-NAME to the 12 standard Program Outcomes (PO1–PO12) defined by the National Board of Accreditation (NBA) for undergraduate engineering programs. Each mapping includes a justification level (High / Medium / Low) and an explanation grounded in the project's actual implementation.

PLACEHOLDER-PROJECT-NAME is an AI-powered application that detects nutritional deficiencies from images of nails, tongues, and skin using custom-trained CNN models. It features a FastAPI backend serving three TensorFlow/Keras models, a React + Vite frontend with Chart.js visualizations, personalized weekly diet plan generation, and a geolocation-based nearby doctors locator using OpenStreetMap's Overpass API.

---

## P-PO Mapping Table

| Project Code | Program Outcome | Level | Justification |
|:---:|:---|:---:|:---|
| PLACEHOLDER-PROJECT-NAME | **PO1: Engineering Knowledge** | **H** | The project applies knowledge from multiple engineering domains: deep learning (CNN-based image classification using TensorFlow/Keras), image processing (BGR→RGB conversion via OpenCV, spatial resizing to 224×224, float32 normalization), web systems (REST API design with FastAPI, React component-based UI with React Router), and software design (service-oriented architecture with `PredictorService` and `DietPlannerService`). Mathematical concepts include softmax probability distributions for multi-class classification and the Haversine formula for distance calculations in the Nearby Doctors feature. |
| PLACEHOLDER-PROJECT-NAME | **PO2: Problem Analysis** | **H** | The team identified the problem of detecting early-stage vitamin deficiencies from visible body part changes. This was decomposed into: (1) separate CNN models for three anatomically distinct body parts (Nail, Tongue, Skin), (2) mapping model outputs to vitamin deficiency labels via configuration dictionaries (`CLASSES`, `DISEASES`), (3) generating dietary recommendations from a curated 14-category food recommendation database (`FOOD_RECOMMENDATIONS` in `config.py`), and (4) connecting users to nearby medical facilities via the Overpass API. Real-world constraints addressed include inference latency (measured at 92–146ms), memory footprint (77–579 MB per model), and input validation (restricting uploads to JPEG/PNG). |
| PLACEHOLDER-PROJECT-NAME | **PO3: Design/Development of Solutions** | **H** | The system is designed as a decoupled client-server application: a React + Vite SPA communicating with a FastAPI REST backend. The backend uses a layered service architecture — `PredictorService` manages model lifecycle (loading `.keras` files at startup via FastAPI's `asynccontextmanager` lifespan), `DietPlannerService` generates 7-day meal plans using cyclic indexing over curated food lists, and the `analysis` router orchestrates the pipeline from image validation through prediction to diet plan generation. The frontend implements React Router with nested layouts (`<Outlet />`), dedicated analysis pages per body part, drag-and-drop image upload via `ImageUploader`, Chart.js confidence bar charts via `ConfidenceChart`, tabbed diet plan display via `DietPlan`, and interactive Leaflet maps via `NearbyDoctors`. When a model file is unavailable, the system falls back to mock predictions using `numpy.random.dirichlet`. |
| PLACEHOLDER-PROJECT-NAME | **PO4: Conduct Investigations** | **H** | The project includes dedicated evaluation scripts: (1) `benchmark_models.py` measures disk size, RAM delta after loading (via `psutil`), model load time, and average inference latency across 10 iterations with warm-up — producing quantitative metrics (Nail: 93.11ms, Tongue: 92.67ms, Skin: 145.53ms); (2) `evaluate_accuracy.py` iterates over held-out test datasets (Nail: 134 samples across 3 classes, Tongue: 76 samples across 2 classes, Skin: 280 samples across 2 classes), computing per-class accuracy with folder-based ground truth matching. Results show the Skin model achieving 98.57% accuracy on Acne while the Nail model's No Disease class achieves only 35.93%, identifying clear areas for improvement. |
| PLACEHOLDER-PROJECT-NAME | **PO5: Modern Tool Usage** | **H** | The project uses: **TensorFlow 2.16.1** for model inference; **FastAPI 0.115.0** with Pydantic validation and automatic Swagger docs; **React 18.3.1** with **Vite 5.4.0** for fast HMR development; **OpenCV 4.10.0** (headless) for image preprocessing; **Chart.js 4.4.4** via `react-chartjs-2` for bar charts; **Leaflet 1.9.4** with `react-leaflet` for interactive maps; **Axios 1.7.7** for HTTP communication; **React Router DOM 7.14.2** for client-side routing; **Pydantic Settings 2.4.0** for configuration with `.env` support; and **psutil** for memory profiling. |
| PLACEHOLDER-PROJECT-NAME | **PO6: The Engineer and Society** | **M** | The project makes preliminary nutritional screening accessible via a free, locally-running tool. All image processing happens in-memory with no persistent storage, ensuring privacy. The application includes a medical disclaimer ("VitaDetect is designed to provide helpful insights, not medical advice") on the home page. The Nearby Doctors feature connects users to nearby hospitals/clinics using real-time OpenStreetMap data. When models produce mock predictions (due to missing files), the system explicitly flags this so users are not misled. |
| PLACEHOLDER-PROJECT-NAME | **PO7: Environment and Sustainability** | **L** | The project uses compact CNN models (73–273 MB) that run on consumer CPUs, avoiding the energy cost of cloud GPU clusters. The local-first architecture eliminates network round-trips for inference. The `FOOD_RECOMMENDATIONS` data promotes whole-food nutrition including vegetables, lentils, and plant-based options. |
| PLACEHOLDER-PROJECT-NAME | **PO8: Ethics** | **M** | Predictions include confidence percentages for transparency rather than binary diagnoses. Mock predictions are labeled: "The model could not be loaded. These results are simulated." No personally identifiable information is collected or stored. The Nearby Doctors component states "Your location data is only used locally and is never stored." Location data is processed client-side and never sent to the backend. |
| PLACEHOLDER-PROJECT-NAME | **PO9: Individual and Teamwork** | **H** | The project was developed by a team of four members (PLACEHOLDER-TEAM-MEMBER-1 through PLACEHOLDER-TEAM-MEMBER-4) under PLACEHOLDER-FACULTY. The modular architecture — separate service classes, isolated React components, and a clean API contract between frontend and backend — supports parallel development. Git version control was used with a structured repository layout separating `backend/`, `frontend/`, `model training/`, and `documentation/` directories. |
| PLACEHOLDER-PROJECT-NAME | **PO10: Communication** | **M** | Code documentation includes Python docstrings with `Args` and `Returns` blocks (e.g., `PredictorService.predict()`, `DietPlannerService.generate_weekly_plan()`), JSDoc comments on the frontend API client (`analyzeImage()` with `@param` and `@returns`), and inline comments. FastAPI auto-generates Swagger/OpenAPI documentation at `/docs`. The UI provides contextual tips ("Tips for best results: Use a well-lit photo of a bare nail, no polish"), descriptive error messages, and ARIA labels for accessibility. |
| PLACEHOLDER-PROJECT-NAME | **PO11: Project Management and Finance** | **M** | The project uses exclusively open-source technologies — TensorFlow (Apache 2.0), FastAPI (MIT), React (MIT), OpenCV (Apache 2.0), Leaflet (BSD), Chart.js (MIT) — with zero licensing costs. Model training used free cloud compute resources (Google Colab/Kaggle Notebooks). The local deployment model avoids recurring cloud compute charges. |
| PLACEHOLDER-PROJECT-NAME | **PO12: Lifelong Learning** | **M** | The project gives the team practical experience with CNN training pipelines, FastAPI async architecture, React component patterns with hooks (`useState`, `useEffect`, `useRef`, `useContext`), and client-side routing. The `models.md` roadmap outlines five additional detection modules (Hair, Lips, Gums, Facial Pallor, Retina), and `suggestions.md` proposes future enhancements including Explainable AI (Grad-CAM), Federated Learning, and GAN-based data augmentation — encouraging continuous learning. |

---

## Mapping Summary

| PO | Level | Primary Evidence |
|:---:|:---:|:---|
| PO1 | H | CNN inference, image processing, REST API, Haversine algorithm |
| PO2 | H | Problem decomposition, constraint analysis, 14-category food database |
| PO3 | H | Client-server architecture, service-oriented backend, React component tree |
| PO4 | H | benchmark_models.py, evaluate_accuracy.py with measured per-class results |
| PO5 | H | TensorFlow, FastAPI, React, Vite, OpenCV, Chart.js, Leaflet, Axios |
| PO6 | M | Privacy-preserving design, medical disclaimers, Nearby Doctors |
| PO7 | L | Lightweight local models, plant-based diet recommendations |
| PO8 | M | Confidence transparency, mock prediction labeling, no PII |
| PO9 | H | 4-member team, Git, modular architecture |
| PO10 | M | Docstrings, OpenAPI docs, ARIA labels, contextual tips |
| PO11 | M | All open-source stack, free compute, local deployment |
| PO12 | M | Transferable skills, extensible architecture, future roadmap |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
