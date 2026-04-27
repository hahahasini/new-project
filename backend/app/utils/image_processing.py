import numpy as np
import cv2
from typing import Tuple


def decode_image(file_bytes: bytes) -> np.ndarray:
    """
    Decode raw bytes into an RGB numpy array.

    Args:
        file_bytes: Raw image bytes.

    Returns:
        RGB numpy array.

    Raises:
        ValueError: If the image cannot be decoded.
    """
    nparr = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image from provided bytes.")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def resize_image(image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    """Resize an image to the given (width, height)."""
    return cv2.resize(image, size)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize pixel values to [0, 1] float32."""
    return image.astype(np.float32) / 255.0


def preprocess_for_model(image: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Full preprocessing pipeline: resize → normalize → add batch dimension.

    Args:
        image: RGB numpy array.
        size: Target (width, height).

    Returns:
        4D numpy array ready for model.predict().
    """
    img = resize_image(image, size)
    img = normalize_image(img)
    return np.expand_dims(img, axis=0)
