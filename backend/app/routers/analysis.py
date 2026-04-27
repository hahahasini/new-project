import numpy as np
import cv2
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.config import settings, ALL_BODY_PARTS, AVAILABLE_MODELS
from app.models.schemas import AnalysisResponse, HealthCheckResponse
from app.services.predictor import PredictorService
from app.services.diet_planner import DietPlannerService

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    body_part: str = Form(..., description="Body part type: Nail, Skin, or Tongue"),
):
    """
    Upload an image and specify the body part to receive:
    - Predicted disease
    - Predicted vitamin deficiency with confidence
    - Per-class confidence scores
    - Weekly diet plan recommendation
    """
    # Validate body part
    if body_part not in ALL_BODY_PARTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid body part '{body_part}'. Must be one of: {ALL_BODY_PARTS}",
        )

    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG images are supported.")

    # Read and decode image
    try:
        contents = await file.read()
        file_bytes = np.frombuffer(contents, dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Could not decode image")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # Check if model is available
    has_model = body_part in AVAILABLE_MODELS

    # Predict deficiency and disease
    prediction = PredictorService.predict(image, body_part)

    # Generate diet plan
    diet_data = DietPlannerService.generate_weekly_plan(prediction["deficiency"])

    return AnalysisResponse(
        body_part=body_part,
        disease=prediction["disease"],
        deficiency=prediction["deficiency"],
        confidence=prediction["confidence"],
        prediction_scores=prediction["prediction_scores"],
        weekly_diet_plan=diet_data["weekly_plan"],
        food_recommendations=diet_data["food_recommendations"],
        model_available=has_model,
    )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        models_loaded=PredictorService.is_loaded(),
        version=settings.APP_VERSION,
        available_models=list(AVAILABLE_MODELS),
    )
