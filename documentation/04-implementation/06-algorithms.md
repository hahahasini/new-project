# Core Algorithms

> **Project**: PLACEHOLDER-PROJECT-NAME | **Last Updated**: PLACEHOLDER-YEAR

---

## 1. CNN Image Classification Algorithm

### 1.1 Purpose
Classifies body part images into vitamin deficiency categories using Convolutional Neural Networks.

### 1.2 Algorithm Steps
```
ALGORITHM: CNN_Classify(image, body_part)
INPUT: RGB image (H×W×3), body_part ∈ {"Nail", "Tongue", "Skin"}
OUTPUT: (deficiency, disease, confidence, scores[])

1. PREPROCESS:
   a. img ← RESIZE(image, 224, 224)         // Spatial normalization
   b. img ← img / 255.0                      // Pixel normalization to [0,1]
   c. tensor ← EXPAND_DIMS(img, axis=0)      // Add batch: (1,224,224,3)

2. INFERENCE:
   a. model ← MODELS[body_part]              // Select body-part model
   b. probs ← model.PREDICT(tensor)          // Forward pass → softmax
   c. probs ← probs[0][:num_classes]         // Trim to known classes

3. CLASSIFICATION:
   a. idx ← ARGMAX(probs)                    // Highest probability index
   b. confidence ← MAX(probs) × 100          // Percentage
   c. deficiency ← CLASSES[body_part][idx]    // Map to label
   d. disease ← DISEASES[body_part][idx]      // Map to disease

4. SCORES:
   a. FOR EACH (i, label) IN CLASSES[body_part]:
        scores.APPEND({label, probs[i] × 100})

5. RETURN (deficiency, disease, confidence, scores)
```

### 1.3 Complexity Analysis
| Aspect | Complexity | Notes |
|:---|:---:|:---|
| Time | O(n²·k) | n=image dimension, k=filter count; dominated by convolution operations |
| Space | O(M) | M=model parameters (~10-70M depending on architecture) |
| Preprocessing | O(n²) | Resize + normalize over all pixels |
| Post-processing | O(c) | c=number of classes (2-3) |
| Total inference | ~92-146 ms | Practical measurement |

---

## 2. Cyclic Diet Plan Generation Algorithm

### 2.1 Purpose
Generates a deterministic 7-day meal plan from a fixed set of meal recommendations.

### 2.2 Pseudocode
```
ALGORITHM: GenerateWeeklyPlan(deficiency)
INPUT: deficiency string (e.g., "Vitamin D Deficiency")
OUTPUT: weekly_plan[7], food_recommendations[]

1. foods ← FOOD_RECOMMENDATIONS[deficiency]
   IF foods IS EMPTY:
       RETURN default_empty_plan

2. DAYS ← ["Monday", ..., "Sunday"]

3. FOR i ← 0 TO 6:
   a. breakfast ← foods["breakfast"][i MOD len(foods["breakfast"])]
   b. lunch     ← foods["lunch"][i MOD len(foods["lunch"])]
   c. dinner    ← foods["dinner"][i MOD len(foods["dinner"])]
   d. weekly_plan[i] ← {day: DAYS[i], meals: {breakfast, lunch, dinner}}

4. flat_recs ← ∅
   FOR EACH meal_type IN ["breakfast", "lunch", "dinner"]:
       FOR EACH item IN foods[meal_type]:
           IF item ∉ flat_recs:
               flat_recs.ADD(item)

5. RETURN {weekly_plan, food_recommendations: flat_recs}
```

### 2.3 Complexity Analysis
| Aspect | Complexity | Notes |
|:---|:---:|:---|
| Time | O(d + m) | d=7 days, m=total meal items (~12) |
| Space | O(d + m) | Weekly plan + flat recommendations |
| Cyclic indexing | O(1) per day | Modular arithmetic |
| De-duplication | O(m²) | Linear scan for uniqueness (small m) |

### 2.4 Why Cyclic Indexing
With 4 breakfast options and 7 days, cyclic indexing wraps around: Mon=0, Tue=1, Wed=2, Thu=3, Fri=0, Sat=1, Sun=2. This ensures variety without requiring 7 unique meals per category.

---

## 3. Haversine Distance Algorithm

### 3.1 Purpose
Calculates the great-circle distance between the user's location and each medical facility on Earth's surface.

### 3.2 Formula
```
ALGORITHM: HaversineKm(lat1, lon1, lat2, lon2)
INPUT: Two geographic coordinate pairs (decimal degrees)
OUTPUT: Distance in kilometers

1. R ← 6371 km                    // Earth's mean radius
2. φ₁ ← lat1 × π / 180           // Convert to radians
3. φ₂ ← lat2 × π / 180
4. Δφ ← (lat2 - lat1) × π / 180
5. Δλ ← (lon2 - lon1) × π / 180

6. a ← sin²(Δφ/2) + cos(φ₁) × cos(φ₂) × sin²(Δλ/2)
7. c ← 2 × atan2(√a, √(1-a))

8. distance ← R × c
9. RETURN distance
```

### 3.3 JavaScript Implementation
```javascript
function haversineKm(lat1, lon1, lat2, lon2) {
    const toRad = (d) => (d * Math.PI) / 180;
    const R = 6371;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}
```

### 3.4 Complexity
| Aspect | Complexity |
|:---|:---:|
| Time | O(1) per calculation |
| Per doctor list | O(n) for n doctors |
| Accuracy | ~0.5% error (assumes spherical Earth) |

---

## 4. Softmax Probability Distribution

### 4.1 Purpose
Converts raw model logits into a probability distribution where all values sum to 1.

### 4.2 Formula
```
σ(z)ᵢ = e^(zᵢ) / Σⱼ e^(zⱼ)

WHERE:
  z = raw output vector from last dense layer
  i = class index
  j = all class indices
```

### 4.3 Example
```
Raw logits: [-1.2, -3.0, 1.8]
Exponentials: [0.30, 0.05, 6.05]
Sum: 6.40
Softmax: [0.047, 0.008, 0.945]
→ Class 2 selected with 94.5% confidence
```

---

## 5. Pseudo-Random Rating Generation

### 5.1 Purpose
Generates deterministic, seeded ratings for hospital/clinic results from OpenStreetMap (which doesn't store ratings).

### 5.2 Algorithm
```
ALGORITHM: GenerateRating(osm_id)
INPUT: OpenStreetMap element ID (integer)
OUTPUT: Rating (3.2–5.0) and review count (20–500)

1. seed ← osm_id MOD 1000
2. rating ← 3.2 + (seed MOD 18) / 10    // Range: 3.2 to 5.0
3. reviewCount ← 20 + (osm_id MOD 480)   // Range: 20 to 500

RETURN (rating, reviewCount)
```

### 5.3 Properties
- **Deterministic**: Same OSM ID always produces the same rating
- **Uniform-looking**: Ratings appear natural (3.2-5.0 range)
- **No external dependency**: No real ratings API needed

---

## 6. Optimization Techniques

### 6.1 Singleton Model Loading
Models loaded once at startup, stored as class attributes, shared across all requests. Avoids per-request model loading (which would take 0.5-2s each time).

### 6.2 In-Memory Image Processing
Images processed entirely in RAM (NumPy arrays), never written to disk. Pipeline: bytes → decode → preprocess → predict → discard.

### 6.3 Batch Dimension Management
TensorFlow expects 4D input (batch, height, width, channels). Single images get `np.expand_dims(img, axis=0)` to add batch=1 dimension, avoiding unnecessary batch creation overhead.

### 6.4 Verbose Suppression
`model.predict(img_array, verbose=0)` prevents TensorFlow from printing progress bars for single-image inference, eliminating I/O overhead.

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
