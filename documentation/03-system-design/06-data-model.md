# Data Model

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

PLACEHOLDER-PROJECT-NAME uses a **configuration-driven data model** rather than a traditional relational database. All domain data — body part classifications, disease mappings, vitamin deficiency labels, and food recommendations — is defined in Python dictionaries within `config.py`. API request/response schemas are enforced via Pydantic models in `schemas.py`. Frontend state is managed through React's `useState` and Context API.

See also: [Data Model Diagram](../diagrams/data-model.puml)

---

## 1. Backend Configuration Data Model

### 1.1 Settings (Application Configuration)

```python
class Settings(BaseSettings):
    APP_NAME: str = "Vitamin Deficiency Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    BASE_DIR: Path              # Project root
    MODELS_DIR: Path            # backend/models/
    NAIL_MODEL: str             # "nail/Nail_epoch_24.keras"
    TONGUE_MODEL: str           # "tongue/Tongue_epoch_01.keras"
    SKIN_MODEL: str             # "skin/skin_disease_model_epoch_46.keras"
    DEFAULT_IMG_SIZE: tuple     # (224, 224)
    CORS_ORIGINS: list[str]     # Allowed frontend origins
```

### 1.2 Body Part Registry

```python
BODY_PARTS = ["Nail", "Skin", "Tongue"]
ALL_BODY_PARTS = ["Nail", "Skin", "Tongue"]
AVAILABLE_MODELS = {"Nail", "Skin", "Tongue"}
```

### 1.3 Classification Labels (CLASSES)

Maps each body part to its vitamin deficiency class labels. The index order matches the model's output layer.

| Body Part | Index 0 | Index 1 | Index 2 |
|:---|:---|:---|:---|
| **Nail** | No Vitamin Deficiency | Iodine Deficiency | Vitamin D Deficiency |
| **Tongue** | Vitamin B12 Deficiency | Iron Deficiency | — |
| **Skin** | Vitamin D Deficiency | Vitamin A Deficiency | — |

### 1.4 Disease Labels (DISEASES)

Maps each body part to human-readable disease names. Index-aligned with CLASSES.

| Body Part | Index 0 | Index 1 | Index 2 |
|:---|:---|:---|:---|
| **Nail** | No disease | Bluish nails | Alopecia areata |
| **Tongue** | Diabetes | Pale tongue | — |
| **Skin** | Acne | Carcinoma | — |

### 1.5 Food Recommendations (FOOD_RECOMMENDATIONS)

A dictionary mapping deficiency names to meal recommendations. Each entry contains three arrays (breakfast, lunch, dinner) with 3-4 meal suggestions each.

**Supported Deficiency Categories** (14 total):

| # | Deficiency Key | Breakfast Entries | Lunch Entries | Dinner Entries |
|:---:|:---|:---:|:---:|:---:|
| 1 | Vitamin A Deficiency | 4 | 4 | 4 |
| 2 | Vitamin B Deficiency | 4 | 4 | 4 |
| 3 | Iron Deficiency | 4 | 4 | 4 |
| 4 | Zinc Deficiency | 4 | 4 | 4 |
| 5 | Vitamin B3 Deficiency | 4 | 4 | 4 |
| 6 | Thyroid issues | 4 | 4 | 4 |
| 7 | Vitamin D Deficiency | 4 | 4 | 4 |
| 8 | Low serum vitamin levels | 4 | 4 | 4 |
| 9 | Iodine Deficiency | 4 | 4 | 4 |
| 10 | Vitamin C Deficiency | 4 | 4 | 4 |
| 11 | Vitamin E Deficiency | 4 | 4 | 4 |
| 12 | Omega-3 Deficiency | 4 | 4 | 4 |
| 13 | Vitamin B12 Deficiency | 4 | 4 | 4 |
| 14 | No Vitamin Deficiency | 1 | 1 | 1 |

**Example Entry** (Vitamin D Deficiency):
```python
"Vitamin D Deficiency": {
    "breakfast": [
        "Oatmeal with fortified plant milk",
        "Mushroom and potato hash",
        "Quinoa porridge with sliced bananas",
        "Chia pudding made with fortified juice"
    ],
    "lunch": [
        "Mushroom and lentil soup",
        "Roasted vegetable salad",
        "Chickpea and spinach bowl",
        "White bean and mushroom stew"
    ],
    "dinner": [
        "Sauteed mushrooms with brown rice",
        "Lentil and vegetable dahl",
        "Baked potato with roasted mushrooms",
        "Mushroom risotto (dairy-free)"
    ]
}
```

---

## 2. API Response Schemas (Pydantic Models)

### 2.1 PredictionScore
```python
class PredictionScore(BaseModel):
    label: str          # e.g., "Vitamin D Deficiency"
    confidence: float   # e.g., 83.05
```

### 2.2 Meals
```python
class Meals(BaseModel):
    breakfast: list[str]    # e.g., ["Oatmeal with fortified plant milk"]
    lunch: list[str]        # e.g., ["Mushroom and lentil soup"]
    dinner: list[str]       # e.g., ["Sauteed mushrooms with brown rice"]
```

### 2.3 DietDay
```python
class DietDay(BaseModel):
    day: str        # "Monday" through "Sunday"
    meals: Meals    # Nested Meals object
```

### 2.4 DeficiencyDietPlan
```python
class DeficiencyDietPlan(BaseModel):
    deficiency: str                      # e.g., "Vitamin D Deficiency"
    confidence: float                    # e.g., 83.05
    weekly_plan: list[DietDay]           # 7 DietDay objects
    food_recommendations: list[str]      # Flat list of recommended foods
```

### 2.5 AnalysisResponse (Primary API Response)
```python
class AnalysisResponse(BaseModel):
    body_part: str                           # "Nail", "Tongue", or "Skin"
    disease: str                             # e.g., "Alopecia areata"
    deficiency: str                          # e.g., "Vitamin D Deficiency"
    confidence: float                        # 0.0–100.0 (percentage)
    prediction_scores: list[PredictionScore] # Per-class confidence breakdown
    weekly_diet_plan: list[DietDay]          # 7-day plan for top deficiency
    food_recommendations: list[str]          # Flat food list for top deficiency
    all_diet_plans: list[DeficiencyDietPlan] # Diet plans for ALL deficiencies
    model_available: bool                    # True if real model was used
```

### 2.6 HealthCheckResponse
```python
class HealthCheckResponse(BaseModel):
    status: str              # "healthy"
    models_loaded: bool      # True if at least one model loaded
    version: str             # e.g., "1.0.0"
    available_models: list[str]  # e.g., ["Nail", "Skin", "Tongue"]
```

---

## 3. Entity Relationships

```
Settings ──[configures]──> PredictorService ──[loads]──> ML Models
                                                            │
CLASSES ──[maps]──> PredictionScore.label                   │
DISEASES ──[maps]──> AnalysisResponse.disease               │
                                                            │
FOOD_RECOMMENDATIONS ──[feeds]──> DietPlannerService        │
                                       │                    │
                                       ▼                    ▼
                              DeficiencyDietPlan     PredictionScore
                                       │                    │
                                       ▼                    ▼
                              AnalysisResponse ◄────────────┘
```

---

## 4. Frontend State Model

### 4.1 Analysis Page State
| Variable | Type | Initial Value | Purpose |
|:---|:---|:---:|:---|
| `selectedImage` | `File \| null` | `null` | Selected image file |
| `previewUrl` | `string \| null` | `null` | Object URL for image preview |
| `results` | `AnalysisResponse \| null` | `null` | API response data |
| `loading` | `boolean` | `false` | Analysis in progress flag |
| `error` | `string \| null` | `null` | Error message |

### 4.2 NearbyDoctors State
| Variable | Type | Initial Value | Purpose |
|:---|:---|:---:|:---|
| `locationState` | `string` | `"idle"` | Geolocation permission state |
| `userCoords` | `{lat, lon} \| null` | `null` | User's GPS coordinates |
| `doctors` | `Doctor[]` | `[]` | Fetched hospital/clinic data |
| `loading` | `boolean` | `false` | Data fetch in progress |
| `fetchError` | `string \| null` | `null` | API error message |
| `selectedDoctor` | `number \| null` | `null` | Selected doctor card ID |
| `searchRadius` | `number` | `5000` | Search radius in meters |

### 4.3 Theme State (Global Context)
| Variable | Type | Initial Value | Purpose |
|:---|:---|:---:|:---|
| `theme` | `"light" \| "dark"` | `"light"` | Current theme mode |

---

## 5. Data Constraints

| Constraint | Rule |
|:---|:---|
| Body Part Validation | Must be in `["Nail", "Skin", "Tongue"]` |
| Image MIME Type | Must be `image/jpeg`, `image/png`, or `image/jpg` |
| Confidence Range | 0.0–100.0 (percentage) |
| Prediction Scores | Sum to ~100% across all classes |
| Weekly Plan Days | Always 7 (Monday–Sunday) |
| Food Recommendations | De-duplicated across meal types |
| Search Radius | 2000, 5000, 10000, or 20000 meters |
| Doctor Results | Maximum 20 per query |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
