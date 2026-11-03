"""Application configuration using pydantic-settings."""
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- API Authentication ---
    API_KEY: str = "abole-demo-key-change-me"

    # --- Model Paths ---
    MODEL_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "model" / "efficientnet_b0_coffee.onnx")
    LABEL_MAPPING_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "model" / "label_mapping.json")
    DISEASE_INFO_PATH: str = str(Path(__file__).resolve().parent.parent / "data" / "disease_info.json")

    # --- Image Constraints ---
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    MAX_IMAGE_SIZE_MB: float = 10.0
    WARNING_MIN_RESOLUTION_PX: int = 256
    WARNING_MAX_FILE_SIZE_MB: float = 5.0

    # --- Inference ---
    DEMO_MODE: bool = True

    # --- App Metadata ---
    APP_NAME: str = "Abole — Coffee Leaf Disease Detection API"
    APP_VERSION: str = "1.0.0"

    # --- CORS ---
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]


settings = Settings()
