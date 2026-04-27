from pydantic import BaseModel
from typing import Optional


class PredictionScore(BaseModel):
    """A single class prediction with its confidence."""
    label: str
    confidence: float


class DietDay(BaseModel):
    """A single day's diet recommendation."""
    day: str
    foods: list[str]


class DeficiencyDietPlan(BaseModel):
    """Diet plan for a single deficiency."""
    deficiency: str
    confidence: float
    weekly_plan: list[DietDay]
    food_recommendations: list[str]


class AnalysisResponse(BaseModel):
    """Full analysis result returned by /api/analyze."""
    body_part: str
    disease: str
    deficiency: str
    confidence: float
    prediction_scores: list[PredictionScore]
    weekly_diet_plan: list[DietDay]
    food_recommendations: list[str]
    all_diet_plans: list[DeficiencyDietPlan]
    model_available: bool  # Whether a real model was used or mock prediction


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    models_loaded: bool
    version: str
    available_models: list[str]  # Which body part models exist
