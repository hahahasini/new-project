# ML Models Implementation

> **Project**: PLACEHOLDER-PROJECT-NAME | **Framework**: TensorFlow 2.16.1 / Keras

---

## 1. Model Overview

Three CNN models are trained for body-part-specific image classification to detect vitamin deficiencies. The models use **transfer learning** on pre-trained architectures (such as MobileNetV2/ResNet), fine-tuned on clinical image datasets for dermatological and oral features. Training was performed in Jupyter notebooks (`nail disease.ipynb`, `tongue.ipynb`, `skin disease.ipynb`) stored in the `model training/` directory.

| Model | Epochs | Input Shape | Output Classes | Disk Size | RAM Usage |
|:---|:---:|:---|:---:|:---:|:---:|
| Nail CNN | 24 | (224, 224, 3) | 3 | 273.64 MB | 578.79 MB |
| Tongue CNN | 1 | (224, 224, 3) | 2 | 73.89 MB | 92.36 MB |
| Skin CNN | 46 | (224, 224, 3) | 2 | 84.24 MB | 77.89 MB |

---

## 2. Nail CNN Model

**File**: `nail/Nail_epoch_24.keras` (273.64 MB)  
**Training**: 24 epochs of fine-tuning  
**Training Notebook**: `model training/nail disease.ipynb`

### Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | No Disease | No Vitamin Deficiency | 64 | 35.93% (23/64) |
| 1 | Bluish nails | Iodine Deficiency | 36 | 33.33% (12/36) |
| 2 | Alopecia areata | Vitamin D Deficiency | 34 | **97.05%** (33/34) |

### Observations
- Strong performance on Alopecia areata (97.05%) indicating the model learned distinct visual features for this condition
- Low accuracy on No Disease and Bluish nail classes suggests the model needs more training data or augmentation for these categories
- The larger model size (273.64 MB / 578.79 MB RAM) compared to other models may indicate a deeper base architecture

---

## 3. Tongue CNN Model

**File**: `tongue/Tongue_epoch_01.keras` (73.89 MB)  
**Training**: 1 epoch of fine-tuning  
**Training Notebook**: `model training/tongue.ipynb`

### Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | Diabetes | Vitamin B12 Deficiency | 40 | **92.50%** (37/40) |
| 1 | Pale Tongue | Iron Deficiency | 36 | **88.89%** (32/36) |

### Observations
- Achieves strong results with only 1 training epoch, suggesting tongue conditions present clear visual markers that transfer learning captures effectively
- Both classes exceed 85% accuracy
- Smallest model (73.89 MB disk, 92.36 MB RAM) — efficient for deployment

---

## 4. Skin CNN Model

**File**: `skin/skin_disease_model_epoch_46.keras` (84.24 MB)  
**Training**: 46 epochs of fine-tuning  
**Training Notebook**: `model training/skin disease.ipynb`

### Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | Acne | Vitamin D Deficiency | 140 | **98.57%** (138/140) |
| 1 | Carcinoma | Vitamin A Deficiency | 140 | **97.14%** (136/140) |

### Observations
- Near-perfect accuracy on both classes (97-99%)
- Largest test dataset (280 total samples) contributes to reliable evaluation
- 46 training epochs with the smallest RAM usage (77.89 MB) suggests an efficient architecture
- Most memory-efficient model despite the most training

---

## 5. Inference Pipeline

The inference pipeline is implemented in `PredictorService.predict()` (`backend/app/services/predictor.py`):

```python
# 1. Image Preprocessing
img = cv2.resize(image, (224, 224))         # Resize to model input size
img = img.astype(np.float32) / 255.0        # Normalize pixel values to [0, 1]
img_array = np.expand_dims(img, axis=0)     # Add batch dimension: (1, 224, 224, 3)

# 2. Model Prediction
prediction = model.predict(img_array, verbose=0)  # Softmax output probabilities
# Example: prediction[0] = [0.12, 0.05, 0.83]

# 3. Post-processing
deficiency_index = np.argmax(prediction[0])  # Index of highest probability → 2
confidence = np.max(prediction[0]) * 100     # As percentage → 83.0%
deficiency = CLASSES[body_part][2]           # Map index → "Vitamin D Deficiency"
disease = DISEASES[body_part][2]             # Map index → "Aloperia areata"
```

### Pipeline Steps
1. **Resize**: `cv2.resize(image, (224, 224))` — spatial normalization to model's expected input dimensions
2. **Normalize**: `img.astype(np.float32) / 255.0` — scale pixel values from [0, 255] to [0, 1]
3. **Batch expand**: `np.expand_dims(img, axis=0)` — TensorFlow expects 4D tensor (batch, height, width, channels)
4. **Predict**: `model.predict(img_array, verbose=0)` — forward pass through CNN, `verbose=0` suppresses progress output
5. **Classify**: `np.argmax(prediction[0])` — select class with highest softmax probability
6. **Map**: Look up `CLASSES[body_part][index]` and `DISEASES[body_part][index]` for human-readable labels

---

## 6. Inference Performance

Benchmarked using `backend/metric_evaluation/benchmark_models.py` — 10 iterations after 1 warm-up run:

| Model | Avg Inference Latency | Model Load Time |
|:---|:---:|:---:|
| Nail | 93.11 ms | 1.43 s |
| Tongue | 92.67 ms | 474.55 ms |
| Skin | 145.53 ms | 2.02 s |

### Comparison with Cloud LLM Alternatives
| Metric | Custom CNNs | Cloud Multi-modal LLMs |
|:---|:---:|:---:|
| Inference latency | 92–146 ms | 5,000–15,000 ms |
| RAM usage | 77–579 MB | 16,000+ MB |
| Per-request cost | $0 (local) | $0.01–0.10/request |
| Privacy | 100% local | Data sent to cloud |

---

## 7. Model Loading & Deployment

Models are loaded at server startup via FastAPI's lifespan context manager:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    PredictorService.load_models()  # Load all models into _models dict
    yield
```

- **Singleton pattern**: Models stored in `PredictorService._models` class-level dict, shared across all requests
- **Graceful degradation**: If a model file is missing, `predict()` generates mock predictions using `np.random.dirichlet` and sets `used_model = False`
- **No GPU required**: All inference runs on CPU by default; TensorFlow can use CUDA GPUs if available without code changes

### Model Files
| Model | Path | Naming Convention |
|:---|:---|:---|
| Nail | `backend/models/nail/Nail_epoch_24.keras` | `{BodyPart}_epoch_{N}.keras` |
| Tongue | `backend/models/tongue/Tongue_epoch_01.keras` | `{BodyPart}_epoch_{N}.keras` |
| Skin | `backend/models/skin/skin_disease_model_epoch_46.keras` | `skin_disease_model_epoch_{N}.keras` |

To update a model: replace the `.keras` file → restart the backend server → models auto-load.

---

## 8. Accuracy Evaluation

Evaluated using `backend/metric_evaluation/evaluate_accuracy.py` against held-out test datasets:

| Model | Total Test Samples | Overall Accuracy |
|:---|:---:|:---:|
| Nail | 134 (3 classes) | ~51.5% |
| Tongue | 76 (2 classes) | ~90.8% |
| Skin | 280 (2 classes) | ~97.9% |

The evaluation script loads each model, iterates over class-specific test folders, preprocesses each image (resize, normalize), runs inference, and compares the predicted class against the folder-based ground truth label.

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
