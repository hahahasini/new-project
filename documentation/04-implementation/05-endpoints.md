# API Endpoints Reference

> **Project**: PLACEHOLDER-PROJECT-NAME | **Base URL**: `http://localhost:8000`

---

## 1. Endpoint Summary

| # | Method | Path | Description | Auth | Rate Limit |
|:---:|:---|:---|:---|:---:|:---:|
| 1 | `GET` | `/` | Root info | None | None |
| 2 | `POST` | `/api/analyze` | Image analysis | None | None |
| 3 | `GET` | `/api/health` | Health check | None | None |

---

## 2. Endpoint Details

### EP-1: Root Info (`GET /`)

**Request**: No parameters  
**Response** (200):
```json
{"app": "Vitamin Deficiency Detection API", "version": "1.0.0", "docs": "/docs"}
```

---

### EP-2: Image Analysis (`POST /api/analyze`)

**Content-Type**: `multipart/form-data`

**Parameters**:
| Name | Type | Required | Values |
|:---|:---|:---:|:---|
| `file` | File | ✅ | JPEG/PNG image |
| `body_part` | String | ✅ | `"Nail"`, `"Skin"`, `"Tongue"` |

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@nail.jpg" -F "body_part=Nail"
```

**Success Response** (200):
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
        {"day": "Monday", "meals": {"breakfast": ["..."], "lunch": ["..."], "dinner": ["..."]}}
    ],
    "food_recommendations": ["Oatmeal with fortified plant milk", "..."],
    "all_diet_plans": [
        {"deficiency": "Vitamin D Deficiency", "confidence": 83.05, "weekly_plan": [], "food_recommendations": []}
    ],
    "model_available": true
}
```

**Error Responses**:
| Code | Condition | Body |
|:---:|:---|:---|
| 400 | Invalid body part | `{"detail": "Invalid body part 'Face'. Must be one of: ['Nail', 'Skin', 'Tongue']"}` |
| 400 | Invalid MIME type | `{"detail": "Only JPEG and PNG images are supported."}` |
| 400 | Corrupted image | `{"detail": "Invalid image file: Could not decode image"}` |
| 422 | Missing field | `{"detail": [{"loc": ["body", "file"], "msg": "field required"}]}` |

---

### EP-3: Health Check (`GET /api/health`)

**Request**: No parameters  
**Response** (200):
```json
{
    "status": "healthy",
    "models_loaded": true,
    "version": "1.0.0",
    "available_models": ["Nail", "Skin", "Tongue"]
}
```

---

## 3. External API: Overpass (Client-Side)

Called directly from the browser (not through backend):

**Endpoint**: `POST https://overpass-api.de/api/interpreter`  
**Content-Type**: `application/x-www-form-urlencoded`

**Query** (OverpassQL):
```
[out:json][timeout:25];
(
  node["amenity"="hospital"](around:5000,17.385,78.487);
  node["amenity"="clinic"](around:5000,17.385,78.487);
  node["amenity"="doctors"](around:5000,17.385,78.487);
  node["healthcare"="doctor"](around:5000,17.385,78.487);
  way["amenity"="hospital"](around:5000,17.385,78.487);
);
out body center 30;
```

**Response**: JSON with `elements[]` array containing OSM nodes/ways with tags.

---

## 4. Error Response Format

All backend errors follow FastAPI's standard format:
```json
{
    "detail": "Human-readable error message"
}
```

Validation errors (422) include field locations:
```json
{
    "detail": [
        {
            "loc": ["body", "body_part"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

---

## 5. API Testing

### Swagger UI (Interactive)
Navigate to `http://localhost:8000/docs` for interactive API testing with "Try it out" functionality.

### Health Check Test
```bash
curl http://localhost:8000/api/health | python -m json.tool
```

### Analysis Test
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@test_nail.jpg" \
  -F "body_part=Nail" | python -m json.tool
```

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
