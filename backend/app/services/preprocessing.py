"""Image preprocessing service for coffee leaf disease detection."""
import io
from typing import List, Tuple

import numpy as np
from PIL import Image

from app.config import settings

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
TARGET_SIZE = (224, 224)


class PreprocessingService:
    def __init__(self):
        self.allowed_types = settings.ALLOWED_IMAGE_TYPES
        self.warning_min_resolution = settings.WARNING_MIN_RESOLUTION_PX
        self.warning_max_file_size = settings.WARNING_MAX_FILE_SIZE_MB * 1024 * 1024

    def process_image(self, image_bytes: bytes) -> Tuple[np.ndarray, List[str]]:
        from app.core.exceptions import InvalidImageError

        warnings: List[str] = []

        if len(image_bytes) > self.warning_max_file_size:
            warnings.append(
                f"Image file size is {len(image_bytes) / 1024 / 1024:.1f}MB "
                f"(recommended max: {settings.WARNING_MAX_FILE_SIZE_MB}MB). "
                "Processing continued but quality may be affected."
            )

        try:
            img = Image.open(io.BytesIO(image_bytes))
        except Exception:
            raise InvalidImageError("Could not open the uploaded file. Please provide a valid image (JPG, PNG, or WEBP).")

        fmt = img.format.upper() if img.format else ""
        if fmt == "JPEG":
            content_type = "image/jpeg"
        elif fmt == "PNG":
            content_type = "image/png"
        elif fmt == "WEBP":
            content_type = "image/webp"
        else:
            raise InvalidImageError(f"Unsupported image format: {fmt}. Please provide a JPG, PNG, or WEBP image.")

        if img.mode != "RGB":
            img = img.convert("RGB")

        width, height = img.size
        min_dim = min(width, height)
        if min_dim < self.warning_min_resolution:
            warnings.append(
                f"Image resolution is {width}x{height}px. "
                f"Minimum recommended resolution is {self.warning_min_resolution}px on the shortest side. "
                "Prediction quality may be reduced."
            )

        aspect = max(width, height) / min(width, height)
        if aspect > 3.0:
            warnings.append(
                f"Image has an unusual aspect ratio ({aspect:.1f}:1). "
                "Ensure the leaf is the main subject of the image."
            )

        img = img.resize(TARGET_SIZE, Image.BILINEAR)
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = (img_array - IMAGENET_MEAN) / IMAGENET_STD
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)

        return img_array, warnings


preprocessing_service = PreprocessingService()
