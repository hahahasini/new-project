# API Specification

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Base URL**: `http://localhost:8000`

---

## Overview

PLACEHOLDER-PROJECT-NAME exposes a RESTful API via FastAPI with automatic OpenAPI/Swagger documentation at `/docs`. The API has two primary endpoints: image analysis and health check. This document provides the complete specification including request/response formats, error codes, and usage examples.

---

## 1. API Endpoints Summary

| Method | Path | Description | Auth |
|:---|:---|:---|:---:|
| `GET` | `/` | Root endpoint — returns app info | None |
| `POST` | `/api/analyze` | Upload image for vitamin deficiency analysis | None |
| `GET` | `/api/health` | Health check and model status | None |

---

## 2. Root Endpoint

### `GET /`

**Description**: Returns basic application information.

**Response** (200 OK):
```json
{
    "app": "Vitamin Deficiency Detection API",
    "version": "1.0.0",
    "docs": "/docs"
}
```

---

## 3. Image Analysis Endpoint

### `POST /api/analyze`

**Description**: Upload an image of a body part (nail, tongue, or skin) to receive:
- Predicted disease condition
- Predicted vitamin deficiency with confidence score
- Per-class confidence score breakdown
- Personalized 7-day weekly diet plan
- Diet plans for all detected deficiencies
- Whether a real model or mock prediction was used

**Content-Type**: `multipart/form-data`

#### Request Parameters

| Parameter | Type | Location | Required | Description |
|:---|:---|:---|:---:|:---|
| `file` | `UploadFile` | Form data | ✅ | Image file (JPEG or PNG) |
| `body_part` | `string` | Form data | ✅ | Body part type: `"Nail"`, `"Skin"`, or `"Tongue"` |

#### Request Headers
```
Content-Type: multipart/form-data
```

#### Example Request (cURL)
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/nail_image.jpg" \
  -F "body_part=Nail"
```

#### Example Request (JavaScript/Axios)
```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('body_part', 'Nail');

const response = await axios.post('http://localhost:8000/api/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000
});
```

#### Success Response (200 OK)
```json
{
    "body_part": "Nail",
    "disease": "Aloperia areata",
    "deficiency": "Vitamin D Deficiency",
    "confidence": 83.05,
    "prediction_scores": [
        {"label": "No Vitamin Deficiency", "confidence": 12.30},
        {"label": "Iodine Deficiency", "confidence": 4.65},
        {"label": "Vitamin D Deficiency", "confidence": 83.05}
    ],
    "weekly_diet_plan": [
        {
            "day": "Monday",
            "meals": {
                "breakfast": ["Oatmeal with fortified plant milk"],
                "lunch": ["Mushroom and lentil soup"],
                "dinner": ["Sauteed mushrooms with brown rice"]
            }
        },
        {
            "day": "Tuesday",
            "meals": {
                "breakfast": ["Mushroom and potato hash"],
                "lunch": ["Roasted vegetable salad"],
                "dinner": ["Lentil and vegetable dahl"]
            }
        }
    ],
    "food_recommendations": [
        "Oatmeal with fortified plant milk",
        "Mushroom and potato hash",
        "Quinoa porridge with sliced bananas",
        "Chia pudding made with fortified juice",
        "Mushroom and lentil soup",
        "Roasted vegetable salad",
        "Chickpea and spinach bowl",
        "White bean and mushroom stew",
        "Sauteed mushrooms with brown rice",
        "Lentil and vegetable dahl",
        "Baked potato with roasted mushrooms",
        "Mushroom risotto (dairy-free)"
    ],
    "all_diet_plans": [
        {
            "deficiency": "Vitamin D Deficiency",
            "confidence": 83.05,
            "weekly_plan": [],
            "food_recommendations": []
        },
        {
            "deficiency": "Iodine Deficiency",
            "confidence": 4.65,
            "weekly_plan": [],
            "food_recommendations": []
        }
    ],
    "model_available": true
}
```

#### Error Responses

| Status | Condition | Response Body |
|:---:|:---|:---|
| **400** | Invalid body part | `{"detail": "Invalid body part 'Face'. Must be one of: ['Nail', 'Skin', 'Tongue']"}` |
| **400** | Invalid file type | `{"detail": "Only JPEG and PNG images are supported."}` |
| **400** | Image decode failure | `{"detail": "Invalid image file: Could not decode image"}` |
| **422** | Missing required field | `{"detail": [{"loc": ["body", "file"], "msg": "field required", "type": "value_error.missing"}]}` |
| **500** | Internal server error | `{"detail": "Internal Server Error"}` |

---

## 4. Health Check Endpoint

### `GET /api/health`

**Description**: Returns the server's operational status, including whether ML models are loaded and which body parts are supported.

#### Example Request
```bash
curl http://localhost:8000/api/health
```

#### Success Response (200 OK)
```json
{
    "status": "healthy",
    "models_loaded": true,
    "version": "1.0.0",
    "available_models": ["Nail", "Skin", "Tongue"]
}
```

#### Response When Models Failed to Load
```json
{
    "status": "healthy",
    "models_loaded": false,
    "version": "1.0.0",
    "available_models": []
}
```

---

## 5. Response Schema Reference

### AnalysisResponse

| Field | Type | Description |
|:---|:---|:---|
| `body_part` | `string` | The analyzed body part ("Nail", "Skin", "Tongue") |
| `disease` | `string` | Human-readable disease name (e.g., "Alopecia areata") |
| `deficiency` | `string` | Detected vitamin deficiency (e.g., "Vitamin D Deficiency") |
| `confidence` | `float` | Confidence percentage (0.0–100.0) for the top prediction |
| `prediction_scores` | `PredictionScore[]` | Per-class confidence breakdown |
| `weekly_diet_plan` | `DietDay[]` | 7-day meal plan for the top deficiency |
| `food_recommendations` | `string[]` | Flat list of recommended foods |
| `all_diet_plans` | `DeficiencyDietPlan[]` | Diet plans for all detected deficiencies |
| `model_available` | `boolean` | `true` if a real ML model was used; `false` for mock predictions |

### PredictionScore

| Field | Type | Description |
|:---|:---|:---|
| `label` | `string` | Deficiency class label |
| `confidence` | `float` | Confidence percentage for this class |

### DietDay

| Field | Type | Description |
|:---|:---|:---|
| `day` | `string` | Day name ("Monday"–"Sunday") |
| `meals` | `Meals` | Breakfast, lunch, dinner arrays |

### Meals

| Field | Type | Description |
|:---|:---|:---|
| `breakfast` | `string[]` | Breakfast meal recommendations |
| `lunch` | `string[]` | Lunch meal recommendations |
| `dinner` | `string[]` | Dinner meal recommendations |

---

## 6. API Design Decisions

### 6.1 No Authentication
The API runs locally without authentication. For production deployment, add:
- API key middleware for rate limiting
- JWT tokens for user-specific features
- HTTPS via reverse proxy (Nginx)

### 6.2 No Pagination
The API returns all data in a single response since:
- Prediction scores are always 2-3 items
- Diet plans are fixed at 7 days
- All diet plans are typically 2-3 deficiencies

### 6.3 Error Handling Standard
All errors follow FastAPI's default pattern:
```json
{
    "detail": "Human-readable error message"
}
```
Validation errors (422) include the field location and constraint violation details.

### 6.4 API Versioning
Currently at v1.0.0. The API path (`/api/analyze`) does not include a version prefix. Future versions would add `/api/v2/analyze` while maintaining backward compatibility.

---

## 7. Swagger Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

These are auto-generated from the Pydantic schemas and route decorators, providing:
- Request/response schema visualization
- "Try it out" functionality for testing endpoints
- Example values and validation rules

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
