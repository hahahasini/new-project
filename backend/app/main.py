from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analysis
from app.services.predictor import PredictorService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup, release on shutdown."""
    print("🔬 Loading ML models...")
    try:
        PredictorService.load_models()
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"⚠️  Model loading error: {e}")
        print("   The API will run in demo mode with mock predictions.")
    yield
    print("🛑 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Detect vitamin deficiencies from images of nails, tongues, and skin.",
    lifespan=lifespan,
)

# CORS -allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(analysis.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
