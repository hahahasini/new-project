import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    APP_NAME: str = "Vitamin Deficiency Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"

    # Model file names (only models that actually exist)
    NAIL_MODEL: str = "nail/Nail_epoch_24.keras"
    TONGUE_MODEL: str = "tongue/Tongue_epoch_01.keras"
    SKIN_MODEL: str = "skin/skin_disease_model_epoch_46.keras"

    # Image preprocessing
    DEFAULT_IMG_SIZE: tuple = (224, 224)

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# ---------------------------------------------------------------------------
# Domain data: class labels, disease mappings, food recommendations
# ---------------------------------------------------------------------------

BODY_PARTS = ["Nail", "Skin", "Tongue"]
ALL_BODY_PARTS = ["Nail", "Skin", "Tongue"]  # Full list for reference

# Models that are available on disk
AVAILABLE_MODELS = {"Nail", "Skin", "Tongue"}

CLASSES = {
    "Nail": ["No Vitamin Deficiency", "Iodine Deficiency", "Vitamin D Deficiency"],
    "Tongue": ["Vitamin B12 Deficiency", "Iron Deficiency"],
    "Skin": ["Vitamin D Deficiency", "Vitamin A Deficiency"],
}

DISEASES = {
    "Nail": ["No disease", "Bluish nails", "Aloperia areata"],
    "Tongue": ["Diabetes", "Pale tongue"],
    "Skin": ["Acne", "Carcinoma"],
}

FOOD_RECOMMENDATIONS = {
    "Vitamin A Deficiency": ["Carrots", "Sweet Potatoes", "Spinach", "Liver"],
    "Vitamin B Deficiency": ["Eggs", "Milk", "Whole Grains", "Legumes"],
    "Iron Deficiency": ["Red Meat", "Leafy Greens", "Lentils", "Tofu"],
    "Zinc Deficiency": ["Pumpkin Seeds", "Chickpeas", "Cashews", "Dairy Products"],
    "Vitamin B3 Deficiency": ["Avocado", "Mushroom", "Green Peas", "Ginger"],
    "Thyroid issues": ["Spinach", "Berries", "Broccoli", "Banana"],
    "Vitamin D Deficiency": ["Sun Bath", "Mushrooms", "Cheese", "Berries"],
    "Low serum vitamin levels": ["Eggs", "Chickpeas", "Whole Grains", "Tofu"],
    "Iodine Deficiency": ["Leafy Greens", "Whole Grains", "Legume", "Cashew"],
    "Vitamin C Deficiency": ["Citrus Fruits", "Strawberries", "Bell Peppers", "Broccoli"],
    "Vitamin E Deficiency": ["Nuts", "Seeds", "Spinach", "Sunflower Oil"],
    "Omega-3 Deficiency": ["Salmon", "Chia Seeds", "Walnuts", "Flaxseeds"],
    "Vitamin B12 Deficiency": ["Clams", "Liver", "Fortified Cereals", "Dairy Products", "Eggs"],
    "No Vitamin Deficiency": [],
}
