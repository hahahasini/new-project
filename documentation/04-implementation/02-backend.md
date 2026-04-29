# Backend Implementation

> **Project**: PLACEHOLDER-PROJECT-NAME | **Technology**: FastAPI 0.115.0 + Uvicorn 0.30.0

---

## 1. Server Setup

The FastAPI app uses `asynccontextmanager` for model loading at startup. CORS middleware allows requests from `localhost:5173/3000`. The server runs on Uvicorn with `--reload` for development.

```python
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, ...)
app.include_router(analysis.router, prefix="/api")
```

## 2. Routing

| Method | Path | Handler | Description |
|:---|:---|:---|:---|
| `GET` | `/` | `root()` | App info |
| `POST` | `/api/analyze` | `analyze_image()` | Full analysis pipeline |
| `GET` | `/api/health` | `health_check()` | Server status |

The analysis endpoint validates body part and MIME type, decodes/preprocesses the image, runs inference, generates diet plans for all classes, and returns a Pydantic-validated `AnalysisResponse`.

## 3. Service Layer

**PredictorService**: Singleton class with `_models` dict storing loaded Keras models. `load_models()` iterates model paths, loads available `.keras` files. `predict()` preprocesses (resize 224×224 → normalize → batch expand), runs `model.predict()`, applies `argmax` for classification, maps indices to deficiency/disease labels. Missing models use `np.random.dirichlet` for mock predictions.

**DietPlannerService**: Static method `generate_weekly_plan(deficiency)` looks up `FOOD_RECOMMENDATIONS`, builds 7-day plans via cyclic indexing (`foods["breakfast"][i % len]`), and flattens unique food recommendations.

## 4. Security

No authentication (local deployment). Input validation via allowlists. Images processed in-memory only — never stored. CORS restricted to known origins. No PII collection.

## 5. Error Handling

- Invalid body part → HTTP 400 with valid options
- Invalid file type → HTTP 400 "Only JPEG and PNG supported"
- Image decode failure → HTTP 400 with error detail
- Model loading failure → Server starts in demo mode with mock predictions

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
