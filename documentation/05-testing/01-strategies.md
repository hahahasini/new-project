# Test Strategies

> **Project**: PLACEHOLDER-PROJECT-NAME | **Last Updated**: PLACEHOLDER-YEAR

---

## 1. Unit Testing

### 1.1 Backend Unit Tests
**Tools**: pytest, pytest-asyncio  
**Coverage Goal**: > 80%

| Module | Test Focus |
|:---|:---|
| `predictor.py` | Model loading, image preprocessing, prediction output format, mock predictions |
| `diet_planner.py` | Weekly plan generation, cyclic indexing, empty deficiency handling, de-duplication |
| `image_processing.py` | decode_image, resize_image, normalize_image, preprocess_for_model |
| `config.py` | Settings validation, CLASSES/DISEASES index alignment, FOOD_RECOMMENDATIONS structure |
| `schemas.py` | Pydantic model validation, serialization, required field enforcement |

### 1.2 Frontend Unit Tests
**Tools**: Vitest, React Testing Library  
**Coverage Goal**: > 75%

| Component | Test Focus |
|:---|:---|
| `api.js` | analyzeImage FormData construction, healthCheck response parsing, error handling |
| `ThemeContext` | Initial theme is light, toggle switches theme, data-theme attribute set |
| `HomePage` | Model cards render, stats display, links navigate correctly |
| `ImageUploader` | Drag-and-drop events, file input trigger, preview rendering |

---

## 2. Integration Testing

| Test Scope | Method |
|:---|:---|
| Frontend ↔ Backend | End-to-end POST /api/analyze with test image; verify response schema |
| Backend ↔ TensorFlow | Load real model, verify prediction output shape and value ranges |
| Router ↔ Services | Verify PredictorService and DietPlannerService integrate correctly |
| CORS Configuration | Verify allowed/blocked origins |

---

## 3. ML Model Validation

### 3.1 Tools
- Custom `evaluate_accuracy.py` script
- Custom `benchmark_models.py` script

### 3.2 Validation Approach
1. Hold-out test datasets (134 + 76 + 280 = 490 samples total)
2. Per-class accuracy measurement with folder-based ground truth
3. Performance benchmarking (disk size, RAM, load time, inference latency)
4. Cross-validation during training (Jupyter notebooks)

### 3.3 Edge Case Testing
- Blurry/low-resolution images
- Rotated/cropped images
- Images with nail polish, tongue coating, skin makeup
- Non-medical images (should return low confidence)

---

## 4. Performance Testing

| Metric | Tool | Target |
|:---|:---|:---|
| API response time | `benchmark_models.py` + cURL timing | < 500ms |
| Model inference latency | `benchmark_models.py` (10 iterations + warm-up) | < 150ms |
| Memory usage | `psutil.Process().memory_info().rss` | < 2GB total |
| Frontend load time | Browser DevTools Lighthouse | FCP < 1.5s |

---

## 5. Security Testing

| Test | Method |
|:---|:---|
| MIME type bypass | Upload non-image file with spoofed content-type |
| Body part injection | Send invalid body_part values (SQL injection, XSS payloads) |
| Large file upload | Upload files > 100MB to test memory limits |
| CORS enforcement | Send requests from unauthorized origins |

---

## 6. Automation

Tests can be integrated into CI/CD via:
```bash
# Backend tests
cd backend && pytest tests/ -v --cov=app --cov-report=html

# Frontend tests  
cd frontend && npx vitest run --coverage

# Model evaluation
cd backend && python -m metric_evaluation.evaluate_accuracy
```

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
