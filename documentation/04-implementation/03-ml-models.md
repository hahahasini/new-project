# ML Models Implementation

> **Project**: PLACEHOLDER-PROJECT-NAME | **Framework**: TensorFlow 2.16.1 / Keras

---

## 1. Model Architecture Overview

Three custom CNNs are trained using **transfer learning** on pre-trained architectures (MobileNetV2/ResNet50), fine-tuned for dermatological and oral image classification.

| Model | Base Architecture | Epochs | Input Shape | Output Classes | Disk Size | RAM |
|:---|:---|:---:|:---|:---:|:---:|:---:|
| Nail CNN | MobileNetV2/ResNet | 24 | (224, 224, 3) | 3 | 273.64 MB | 578.79 MB |
| Tongue CNN | MobileNetV2/ResNet | 1 | (224, 224, 3) | 2 | 73.89 MB | 92.36 MB |
| Skin CNN | MobileNetV2/ResNet | 46 | (224, 224, 3) | 2 | 84.24 MB | 77.89 MB |

---

## 2. Nail CNN Model

### 2.1 Architecture
- **Base**: Pre-trained MobileNetV2/ResNet50 (ImageNet weights, top layers removed)
- **Custom Head**: GlobalAveragePooling2D → Dense(128, ReLU) → Dropout(0.5) → Dense(3, Softmax)
- **Training**: 24 epochs with Adam optimizer, categorical cross-entropy loss
- **File**: `nail/Nail_epoch_24.keras` (273.64 MB)

### 2.2 Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | No Disease | No Vitamin Deficiency | 64 | 35.93% |
| 1 | Bluish nails | Iodine Deficiency | 36 | 33.33% |
| 2 | Alopecia areata | Vitamin D Deficiency | 34 | **97.05%** |

### 2.3 Performance Analysis
The Nail model shows strong performance on Alopecia areata (97%) but struggles with No Disease and Bluish nail classes. This is likely due to: (1) class imbalance in training data, (2) visual similarity between healthy nails and early-stage deficiency, (3) limited dataset size for bluish nail conditions.

---

## 3. Tongue CNN Model

### 3.1 Architecture
- **Base**: Pre-trained MobileNetV2/ResNet50
- **Custom Head**: GlobalAveragePooling2D → Dense(64, ReLU) → Dropout(0.3) → Dense(2, Softmax)
- **Training**: 1 epoch (early convergence due to clear visual features)
- **File**: `tongue/Tongue_epoch_01.keras` (73.89 MB)

### 3.2 Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | Diabetes | Vitamin B12 Deficiency | 40 | **92.50%** |
| 1 | Pale Tongue | Iron Deficiency | 36 | **88.89%** |

### 3.3 Performance Analysis
Tongue analysis achieves excellent results with only 1 training epoch. Tongue conditions present distinctive color/texture changes (pale vs. inflamed) that transfer learning captures effectively.

---

## 4. Skin CNN Model

### 4.1 Architecture
- **Base**: Pre-trained MobileNetV2/ResNet50
- **Custom Head**: GlobalAveragePooling2D → Dense(128, ReLU) → Dropout(0.5) → Dense(2, Softmax)
- **Training**: 46 epochs with extensive augmentation
- **File**: `skin/skin_disease_model_epoch_46.keras` (84.24 MB)

### 4.2 Output Classes
| Index | Disease Label | Deficiency Label | Test Samples | Accuracy |
|:---:|:---|:---|:---:|:---:|
| 0 | Acne | Vitamin D Deficiency | 140 | **98.57%** |
| 1 | Carcinoma | Vitamin A Deficiency | 140 | **97.14%** |

### 4.3 Performance Analysis
The Skin model achieves near-perfect accuracy (97-99%) on both classes. The larger dataset (280 test samples) and 46 training epochs contributed to robust generalization. Acne and carcinoma have distinctly different visual patterns.

---

## 5. Training Details

### 5.1 Data Augmentation
```python
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    fill_mode='nearest',
    rescale=1.0/255.0
)
```

### 5.2 Training Configuration
| Parameter | Value |
|:---|:---|
| Optimizer | Adam (default learning rate 0.001) |
| Loss Function | Categorical Cross-Entropy |
| Batch Size | 32 |
| Image Size | 224 × 224 × 3 |
| Validation Split | ~20% of training data |
| Early Stopping | Monitored val_loss (patience varies) |

### 5.3 Training Environment
- **Platform**: Google Colab / Kaggle Notebooks (free GPU tier)
- **GPU**: NVIDIA T4 / P100 (training only)
- **Notebooks**: `nail disease.ipynb`, `tongue.ipynb`, `skin disease.ipynb`
- **Export**: `.keras` format for TF 2.16 compatibility

---

## 6. Inference Pipeline

```python
# 1. Image Preprocessing
img = cv2.resize(image, (224, 224))         # Resize to model input
img = img.astype(np.float32) / 255.0        # Normalize [0, 1]
img_array = np.expand_dims(img, axis=0)     # Add batch: (1, 224, 224, 3)

# 2. Model Prediction
prediction = model.predict(img_array, verbose=0)  # Softmax output
# prediction[0] = [0.12, 0.05, 0.83]

# 3. Post-processing
deficiency_index = np.argmax(prediction[0])  # → 2
confidence = np.max(prediction[0]) * 100     # → 83.0%
deficiency = CLASSES[body_part][2]           # → "Vitamin D Deficiency"
disease = DISEASES[body_part][2]             # → "Alopecia areata"
```

### 6.1 Inference Latency
| Model | Avg Latency | Load Time |
|:---|:---:|:---:|
| Nail | 93.11 ms | 1.43 s |
| Tongue | 92.67 ms | 474.55 ms |
| Skin | 145.53 ms | 2.02 s |

### 6.2 vs. LLM Alternatives
Custom CNNs execute 50-160× faster than multi-modal LLMs (92-146ms vs 5-15s), use 28-205× less RAM (77-579MB vs 16GB+), cost $0 per request (local vs $0.01-0.10), and provide superior privacy (no cloud data transmission).

---

## 7. Model Deployment

- Models stored in `backend/models/{body_part}/` directory
- Loaded at server startup via `PredictorService.load_models()`
- Shared across all requests (singleton pattern)
- Missing models trigger mock predictions (Dirichlet distribution)
- No GPU required for inference (CPU-only execution)

---

## 8. Model Versioning

| Model | Current Version | Naming Convention |
|:---|:---|:---|
| Nail | Epoch 24 | `Nail_epoch_24.keras` |
| Tongue | Epoch 01 | `Tongue_epoch_01.keras` |
| Skin | Epoch 46 | `skin_disease_model_epoch_46.keras` |

Updates: Replace model file → restart server → models auto-load.

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
