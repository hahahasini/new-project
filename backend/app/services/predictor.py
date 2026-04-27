import numpy as np
import cv2
from typing import Optional

from app.config import settings, CLASSES, DISEASES


class PredictorService:
    """Predicts vitamin deficiency and disease from body-part images."""

    _models: dict = {}
    _loaded: bool = False

    @classmethod
    def load_models(cls):
        """Load all available body-part-specific models."""
        import tensorflow as tf
        import keras

        # Only load models that actually exist on disk
        model_map = {
            "Nail": settings.NAIL_MODEL,
            "Tongue": settings.TONGUE_MODEL,
            "Skin": settings.SKIN_MODEL,
        }

        for part, filename in model_map.items():
            model_path = settings.MODELS_DIR / filename
            if model_path.exists():
                cls._models[part] = keras.models.load_model(str(model_path))
                print(f"  ✅ {part} model loaded from {model_path}")
            else:
                print(f"  ⚠️  {part} model not found at {model_path}")

        cls._loaded = len(cls._models) > 0
        
        # Log which models are missing
        missing = set(model_map.keys()) - set(cls._models.keys())
        if missing:
            print(f"  ℹ️  Models not available for: {', '.join(missing)} (will use mock predictions)")

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._loaded

    @classmethod
    def predict(cls, image: np.ndarray, body_part: str) -> dict:
        """
        Predict deficiency and disease for a given body part image.

        Args:
            image: RGB numpy array.
            body_part: One of "Nail", "Skin", "Tongue".

        Returns:
            Dict with deficiency, confidence, disease, and prediction scores.
        """
        img = cv2.resize(image, settings.DEFAULT_IMG_SIZE)
        img = img.astype(np.float32) / 255.0
        img_array = np.expand_dims(img, axis=0)

        part_classes = CLASSES.get(body_part, [])
        part_diseases = DISEASES.get(body_part, [])

        if body_part in cls._models:
            prediction = cls._models[body_part].predict(img_array, verbose=0)
            prediction_values = prediction[0]
            used_model = True
        else:
            # Mock prediction for body parts without models (Skin)
            num_classes = len(part_classes)
            prediction_values = np.random.dirichlet(np.ones(num_classes))
            used_model = False

        # Trim to number of known classes
        num_classes = len(part_classes)
        prediction_values = prediction_values[:num_classes]

        deficiency_index = int(np.argmax(prediction_values))
        confidence = float(np.max(prediction_values)) * 100

        deficiency = part_classes[deficiency_index] if deficiency_index < len(part_classes) else "Unknown"
        disease = part_diseases[deficiency_index] if deficiency_index < len(part_diseases) else "Unknown"

        # Build per-class scores
        scores = []
        for i, label in enumerate(part_classes):
            scores.append({
                "label": label,
                "confidence": round(float(prediction_values[i]) * 100, 2),
            })

        return {
            "deficiency": deficiency,
            "confidence": round(confidence, 2),
            "disease": disease,
            "prediction_scores": scores,
            "used_model": used_model,
        }
