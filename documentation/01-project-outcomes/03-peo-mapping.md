# Program Educational Objective (PEO) Mapping

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection Using Image Processing and Deep Learning  
> **Institution**: PLACEHOLDER-INSTITUTION | **Year**: PLACEHOLDER-YEAR | **Semester**: PLACEHOLDER-SEMESTER  
> **Team**: PLACEHOLDER-TEAM-MEMBER-1, PLACEHOLDER-TEAM-MEMBER-2, PLACEHOLDER-TEAM-MEMBER-3, PLACEHOLDER-TEAM-MEMBER-4  
> **Faculty Guide**: PLACEHOLDER-FACULTY (PLACEHOLDER-FACULTY-ROLE)

---

## Overview

Program Educational Objectives (PEOs) describe the career and professional accomplishments that graduates are expected to attain within a few years after graduation. This document maps PLACEHOLDER-PROJECT-NAME to 8 PEOs, demonstrating how the project experience prepares graduates for professional success.

---

## P-PEO Mapping Table

| Project Code | PEO | Level | Justification |
|:---:|:---|:---:|:---|
| PLACEHOLDER-PROJECT-NAME | **PEO1: Technical Proficiency** — Graduates will demonstrate competence in applying computer science fundamentals to analyze, design, and implement computing solutions. | **H** | The project applies core CS fundamentals: algorithm design (Haversine distance, cyclic meal plan generation, argmax classification), data structures (NumPy arrays for image tensors, Python dictionaries for configuration mapping, React state hooks), software architecture (client-server separation, service-oriented backend, component-based frontend), and systems programming (async I/O with FastAPI, browser API integration for geolocation and file handling). The ability to integrate TensorFlow inference pipelines with a production-grade web server demonstrates engineering proficiency applicable to industry roles. |
| PLACEHOLDER-PROJECT-NAME | **PEO2: Professional Growth** — Graduates will engage in continuous professional development, adapting to evolving technologies. | **H** | The technology stack reflects current industry choices: FastAPI (rapidly growing for ML-serving applications), React 18 with hooks (dominant frontend paradigm), Vite (next-generation build tooling), and TensorFlow 2.x with Keras API. The team's `models.md` and `suggestions.md` documents propose integrations with Explainable AI (Grad-CAM), Federated Learning for privacy-preserving training, GAN-based synthetic data augmentation, TensorFlow Lite for mobile, and TensorFlow.js for browser inference — demonstrating engagement with emerging technologies. |
| PLACEHOLDER-PROJECT-NAME | **PEO3: Societal Contribution** — Graduates will apply their technical knowledge to address real-world problems responsibly. | **H** | The project provides a free, locally-running screening tool for nutritional health assessment. The Nearby Doctors feature connects users to medical professionals via OpenStreetMap data. The medical disclaimer system ("VitaDetect is designed to provide helpful insights, not medical advice") ensures responsible use. Privacy is preserved by processing images in-memory without storage and running all inference locally without cloud dependencies. |
| PLACEHOLDER-PROJECT-NAME | **PEO4: Communication & Collaboration** — Graduates will communicate effectively and work collaboratively in teams. | **M** | The project develops communication through: (1) code documentation (docstrings, JSDoc comments, inline comments); (2) API documentation (FastAPI auto-generated Swagger at `/docs`); (3) user-facing communication (upload tips, error messages, contextual help); (4) team collaboration across a 4-member team distributed across ML training, backend, frontend, and integration work, coordinated through Git version control. |
| PLACEHOLDER-PROJECT-NAME | **PEO5: Innovation & Entrepreneurship** — Graduates will demonstrate creative thinking and innovative problem-solving. | **M** | Rather than relying on cloud-based multi-modal LLMs for image analysis (which incur per-request costs, latency, and privacy concerns), the team trained compact purpose-specific CNN models that execute 50-160× faster at zero cost. The `suggestions.md` document outlines a product evolution roadmap spanning model improvements, analytics, nutrition, platform expansion, clinical integration, and safety/compliance — demonstrating product-oriented thinking. |
| PLACEHOLDER-PROJECT-NAME | **PEO6: Ethics & Professional Responsibility** — Graduates will practice their profession with ethical integrity. | **H** | Ethical design is embedded: all predictions show confidence percentages rather than binary diagnoses; mock predictions are labeled so users aren't deceived; no PII is collected or stored; location data stays client-side; the accuracy evaluation in `README.md` reports both strong results (98.57% Skin-Acne) and weak ones (33.33% Nail-Bluish) without cherry-picking; and the `suggestions.md` identifies the need for expanded datasets from diverse populations to reduce model bias. |
| PLACEHOLDER-PROJECT-NAME | **PEO7: Research Aptitude** — Graduates will demonstrate ability to engage in systematic investigation. | **M** | Research skills are demonstrated through: (1) model training in Jupyter notebooks with configurable hyperparameters; (2) systematic evaluation with held-out test sets via `evaluate_accuracy.py`; (3) performance benchmarking with controlled methodology (10 iterations + warm-up) via `benchmark_models.py`; (4) per-class accuracy analysis revealing model strengths/weaknesses; (5) the `suggestions.md` document proposing research directions including Grad-CAM explainability and Federated Learning. |
| PLACEHOLDER-PROJECT-NAME | **PEO8: Lifelong Learning & Adaptability** — Graduates will adapt to new technologies and domains. | **M** | The system's extensible design supports ongoing learning: adding a new body part analysis requires placing a model file, adding config entries, and creating a frontend page — documented in `models.md`. The project required learning across ML, web development, image processing, nutritional science, and geolocation services. Skills developed (REST API design, React architecture, CNN pipelines, evaluation methodology) transfer across industries. The 25+ proposed enhancements in `suggestions.md` demonstrate a growth mindset. |

---

## PEO Summary

| PEO | Level | Long-term Professional Impact |
|:---:|:---:|:---|
| PEO1 | H | Engineering fundamentals applicable across computing careers |
| PEO2 | H | Modern stack aligning with industry trends |
| PEO3 | H | Healthcare accessibility with privacy and disclaimers |
| PEO4 | M | Documentation, API specs, team collaboration |
| PEO5 | M | Cost-effective alternative to cloud LLMs with product roadmap |
| PEO6 | H | Transparent predictions, no PII, honest accuracy reporting |
| PEO7 | M | Evaluation scripts, benchmarking methodology, future research |
| PEO8 | M | Extensible architecture, cross-domain skills, enhancement roadmap |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
