# Performance Results

> **Project**: PLACEHOLDER-PROJECT-NAME | **Last Updated**: PLACEHOLDER-YEAR

---

## 1. API Response Times

### 1.1 /api/analyze Endpoint

| Metric | Target | Measured | Status |
|:---|:---:|:---:|:---:|
| Average response time | < 500 ms | ~350–450 ms | ✅ Met |
| 95th percentile | < 2,000 ms | ~600 ms | ✅ Met |
| Maximum (cold start) | < 5,000 ms | ~1,200 ms | ✅ Met |
| Maximum (warm) | < 1,000 ms | ~500 ms | ✅ Met |

### 1.2 /api/health Endpoint

| Metric | Target | Measured | Status |
|:---|:---:|:---:|:---:|
| Average response time | < 50 ms | ~5 ms | ✅ Met |

---

## 2. Model Inference Performance

### 2.1 Inference Latency (10 iterations, 1 warm-up)

| Model | Target | Measured | Disk Size | RAM Delta | Load Time |
|:---|:---:|:---:|:---:|:---:|:---:|
| Nail CNN | < 150 ms | **93.11 ms** | 273.64 MB | 578.79 MB | 1.43 s |
| Tongue CNN | < 150 ms | **92.67 ms** | 73.89 MB | 92.36 MB | 474.55 ms |
| Skin CNN | < 200 ms | **145.53 ms** | 84.24 MB | 77.89 MB | 2.02 s |
| **Total** | — | — | **431.77 MB** | **749.04 MB** | **3.92 s** |

### 2.2 Frontend Page Load Times

| Metric | Target | Measured | Status |
|:---|:---:|:---:|:---:|
| First Contentful Paint | < 1.5 s | ~0.8 s | ✅ Met |
| Time to Interactive | < 3.0 s | ~1.5 s | ✅ Met |
| Largest Contentful Paint | < 2.5 s | ~1.2 s | ✅ Met |
| Cumulative Layout Shift | < 0.1 | ~0.02 | ✅ Met |

---

## 3. Requirement vs. Achievement

| Requirement | Target | Achieved | Delta |
|:---|:---:|:---:|:---:|
| NF1.1: API response time (p95) | < 2 s | ~600 ms | **70% faster** |
| NF1.2: Inference latency (avg) | < 150 ms | 93–146 ms | ✅ Within target |
| NF1.3: Frontend FCP | < 1.5 s | ~0.8 s | **47% faster** |
| NF1.5: Image preview render | < 100 ms | ~10 ms | **90% faster** |
| NF1.9: Model loading time | < 5 s | 3.92 s | ✅ Within target |
| NF5.4: Total RAM for models | < 1 GB | 749 MB | ✅ Within target |

---

## 4. ML Model Performance

### 4.1 Classification Accuracy

| Model | Class | Target | Achieved | Test Samples | Status |
|:---|:---|:---:|:---:|:---:|:---:|
| Nail | No Disease | > 60% | 35.93% | 64 | ⚠️ Below |
| Nail | Bluish nail | > 60% | 33.33% | 36 | ⚠️ Below |
| Nail | Alopecia areata | > 85% | **97.05%** | 34 | ✅ Exceeded |
| Tongue | Diabetes | > 85% | **92.50%** | 40 | ✅ Exceeded |
| Tongue | Pale Tongue | > 85% | **88.89%** | 36 | ✅ Met |
| Skin | Acne | > 90% | **98.57%** | 140 | ✅ Exceeded |
| Skin | Carcinoma | > 90% | **97.14%** | 140 | ✅ Exceeded |

### 4.2 Overall Model Accuracy

| Model | Test Samples | Overall Accuracy |
|:---|:---:|:---:|
| Nail | 134 | ~51.5% |
| Tongue | 76 | ~90.8% |
| Skin | 280 | ~97.9% |

### 4.3 Performance vs. LLMs

| Metric | Custom CNNs | Multi-modal LLMs | Improvement |
|:---|:---:|:---:|:---:|
| Inference latency | 92–146 ms | 5,000–15,000 ms | **50–160× faster** |
| RAM usage | 77–579 MB | 16,000+ MB | **28–205× less** |
| Per-request cost | $0.00 | $0.01–0.10 | **100% savings** |
| Privacy | 100% local | Cloud-dependent | **Superior** |

---

## 5. Load Test Results

| Metric | Result |
|:---|:---|
| Sequential requests per minute | ~150 RPM |
| 5 concurrent requests | All complete within 2s |
| 10 concurrent requests | All complete within 4s |
| Memory under load (10 requests) | Stable at ~800 MB |
| Error rate under load | 0% |

---

## 6. Known Performance Limitations

| Limitation | Impact | Mitigation |
|:---|:---|:---|
| Nail model low accuracy (No Disease, Bluish nail) | False positives/negatives for 2 of 3 classes | Need more diverse training data, longer training |
| Single-threaded TensorFlow inference | Sequential request processing | Use multiple Uvicorn workers |
| Large Nail model (274 MB / 579 MB RAM) | Dominates memory budget | Consider model pruning/quantization |
| Cold start model loading (~4s) | First request delayed | Pre-warm models at startup (already implemented) |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
