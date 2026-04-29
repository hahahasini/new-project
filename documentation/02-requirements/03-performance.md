# Performance Specifications

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document defines the detailed performance specifications for PLACEHOLDER-PROJECT-NAME, covering speed/latency requirements, throughput specifications, resource constraints, ML model performance targets, and real-time processing requirements. All metrics are based on benchmarks conducted using the `benchmark_models.py` and `evaluate_accuracy.py` evaluation scripts included in the project.

---

## 1. Inference Latency Requirements

### 1.1 Model Inference Targets

Each CNN model must execute a single-image inference within the following latency budgets. These benchmarks were measured over 10 iterations after a 1-iteration warm-up on standard hardware.

| Model | Target Latency | Measured Latency | Status |
|:---|:---:|:---:|:---:|
| Nail CNN (MobileNetV2/ResNet, 24 epochs) | < 150 ms | **93.11 ms** | ✅ Met |
| Tongue CNN (MobileNetV2/ResNet, 1 epoch) | < 150 ms | **92.67 ms** | ✅ Met |
| Skin CNN (MobileNetV2/ResNet, 46 epochs) | < 200 ms | **145.53 ms** | ✅ Met |

### 1.2 End-to-End Analysis Pipeline

The complete analysis pipeline — from HTTP request receipt to JSON response — includes image validation, preprocessing, model inference, diet plan generation, and response serialization.

| Stage | Target | Notes |
|:---|:---:|:---|
| Image upload receipt & validation | < 50 ms | MIME type check, body part validation |
| Image decoding (bytes → NumPy) | < 30 ms | OpenCV `imdecode` + BGR→RGB conversion |
| Image preprocessing (resize + normalize) | < 10 ms | Resize to 224×224, float32/255.0, batch expand |
| Model inference | < 150 ms | TensorFlow `model.predict()` with `verbose=0` |
| Post-processing (argmax + mapping) | < 5 ms | NumPy argmax, dictionary lookup |
| Diet plan generation (all classes) | < 20 ms | Cyclic meal assignment for 7 days × N deficiencies |
| Response serialization (Pydantic → JSON) | < 10 ms | Pydantic model validation and JSON encoding |
| **Total pipeline target** | **< 500 ms** | **Measured: ~350-450 ms typical** |

### 1.3 Frontend Rendering Performance

| Metric | Target | Notes |
|:---|:---:|:---|
| First Contentful Paint (FCP) | < 1.5 s | Vite-optimized bundle with ES module loading |
| Time to Interactive (TTI) | < 3.0 s | React hydration with deferred model card images |
| Image preview render | < 100 ms | Client-side `URL.createObjectURL` (no upload) |
| Chart.js render | < 200 ms | Bar chart with 2-3 data points |
| Leaflet map initialization | < 500 ms | CartoDB tile layer with initial viewport |
| Route transition | < 100 ms | Client-side React Router (no page reload) |

---

## 2. Throughput Specifications

### 2.1 Request Throughput

| Metric | Specification |
|:---|:---|
| Max concurrent analysis requests | 5-10 (limited by TensorFlow's thread pool on single CPU) |
| Estimated requests per minute (sequential) | ~120-170 RPM (based on ~350-500ms per request) |
| Health check throughput | > 1000 RPM (minimal processing) |
| Maximum image file size | 10 MB (practical limit; no hard enforcement) |
| Axios request timeout | 60 seconds (accommodates slow cold-start inference) |

### 2.2 External API Throughput

| API | Rate Limit | Mitigation |
|:---|:---:|:---|
| Overpass API (OpenStreetMap) | ~2 requests/second per IP | Queries trigger only on explicit user action or radius change; results cached in React state |
| CartoDB tile server | Standard OSM tile usage policy | Browser caches tiles; `maxZoom: 14` limits tile requests |

---

## 3. Resource Constraints

### 3.1 Model Resource Requirements

| Model | Disk Size | RAM Usage (Delta) | Load Time |
|:---|:---:|:---:|:---:|
| Nail CNN | 273.64 MB | 578.79 MB | 1.43 s |
| Tongue CNN | 73.89 MB | 92.36 MB | 474.55 ms |
| Skin CNN | 84.24 MB | 77.89 MB | 2.02 s |
| **Total** | **431.77 MB** | **~749.04 MB** | **~3.92 s** |

### 3.2 System Resource Requirements

| Resource | Minimum | Recommended |
|:---|:---:|:---:|
| CPU | 2 cores (x86_64) | 4+ cores |
| RAM | 2 GB (models + OS) | 4+ GB |
| Disk | 1 GB (models + code) | 2+ GB (with datasets) |
| GPU | Not required | Optional (CUDA for faster inference) |
| Python | 3.9+ | 3.11+ |
| Node.js | 18+ | 20+ LTS |
| Network | Not required for inference | Required for Nearby Doctors feature |

### 3.3 Frontend Bundle Size

| Asset | Size (estimated) |
|:---|:---:|
| JavaScript bundle (minified + gzipped) | ~200 KB |
| CSS bundle (minified + gzipped) | ~15 KB |
| Leaflet CSS + JS | ~40 KB (gzipped) |
| Chart.js | ~65 KB (gzipped) |
| Total initial page load | ~320 KB (excluding images) |

---

## 4. ML Model Performance Targets

### 4.1 Classification Accuracy Targets

| Model | Class | Target Accuracy | Measured Accuracy | Test Samples | Status |
|:---|:---|:---:|:---:|:---:|:---:|
| Nail | No Disease | > 60% | 35.93% | 64 | ⚠️ Below target |
| Nail | Bluish nail | > 60% | 33.33% | 36 | ⚠️ Below target |
| Nail | Alopecia areata | > 85% | **97.05%** | 34 | ✅ Exceeded |
| Tongue | Diabetes | > 85% | **92.50%** | 40 | ✅ Exceeded |
| Tongue | Pale Tongue | > 85% | **88.89%** | 36 | ✅ Met |
| Skin | Acne | > 90% | **98.57%** | 140 | ✅ Exceeded |
| Skin | Carcinoma | > 90% | **97.14%** | 140 | ✅ Exceeded |

### 4.2 Dataset Evaluation Summary

| Model | Total Test Samples | Overall Accuracy | Weighted F1 (est.) |
|:---|:---:|:---:|:---:|
| Nail | 134 | ~51.5% | ~55.4% |
| Tongue | 76 | ~90.8% | ~90.6% |
| Skin | 280 | ~97.9% | ~97.8% |

### 4.3 Performance vs. LLM Alternatives

| Metric | Custom CNNs | Multi-modal LLMs (GPT-4V) | Advantage |
|:---|:---:|:---:|:---:|
| Inference latency | 92–146 ms | 5,000–15,000 ms | **50-160× faster** |
| RAM usage | 77–579 MB | 16,000+ MB | **28-205× less** |
| Per-request cost | $0 (local) | $0.01–0.10/request | **Free** |
| Privacy | 100% local | Data sent to cloud | **Superior** |
| Specialized accuracy | Trained on medical data | General-purpose | **More focused** |

---

## 5. Real-Time Processing Requirements

### 5.1 User Interaction Responsiveness

| Interaction | Maximum Acceptable Delay |
|:---|:---:|
| File drag-over visual feedback | < 16 ms (single frame at 60fps) |
| Image preview generation | < 100 ms |
| Button state change (loading) | Immediate (< 16 ms) |
| Theme toggle application | < 50 ms (CSS variable swap) |
| Navigation route change | < 100 ms |
| Tab switch (diet plans) | < 50 ms |
| Map marker click → popup | < 100 ms |

### 5.2 Animation Frame Budget

All CSS animations and transitions maintain a 60fps target (16.67ms frame budget):
- Fade-in animations: `animation-duration: 0.5s` with `ease-out` timing
- Slide-in animations: `animation-duration: 0.4s`
- Staggered children: `animation-delay` increments of 0.1s
- Theme transition: CSS `transition: background-color 0.3s, color 0.3s`
- Navbar scroll effect: CSS `transition: background-color 0.3s, box-shadow 0.3s`

---

## 6. Scalability Targets

| Dimension | Current Capacity | Growth Target |
|:---|:---:|:---:|
| Body part models | 3 (Nail, Tongue, Skin) | Up to 8 (Hair, Lips, Gums, Pallor, Retina) |
| Deficiency categories | 14 food recommendation sets | Up to 25+ |
| Concurrent users (local) | 5-10 | N/A (local deployment) |
| Concurrent users (cloud deployment) | N/A | 100+ with load balancer |
| Model file storage | ~432 MB | ~1.5 GB (with 5 additional models) |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
