"""API route definitions for the coffee leaf disease detection API."""
import logging

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.config import settings
from app.core.exceptions import InvalidImageError
from app.core.security import verify_api_key
from app.schemas.prediction import (
    ClassProbability,
    HealthResponse,
    PredictionResponse,
)
from app.services.disease_info import disease_info_service
from app.services.inference import inference_service
from app.services.preprocessing import preprocessing_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint - no authentication required."""
    return HealthResponse(
        status="ok",
        model_loaded=inference_service.model_loaded,
        demo_mode=inference_service.is_demo,
        version=settings.APP_VERSION,
    )


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict coffee leaf disease from an uploaded image",
    description="Upload a coffee leaf image to classify it as Healthy, Cercospora, Leaf Rust, Miner, or Phoma. Requires an API key in the 'X-API-Key' header.",
)
async def predict(
    file: UploadFile = File(..., description="Coffee leaf image file (JPG, PNG, or WEBP)"),
    _api_key: str = Depends(verify_api_key),
):
    """Process an uploaded image and return a disease prediction."""

    file_bytes = await file.read()

    if not file_bytes:
        raise InvalidImageError("No file content received. Please upload a valid image.")

    input_array, warnings = preprocessing_service.process_image(file_bytes)

    predicted_class, confidence, all_probs, is_demo = inference_service.predict(input_array)

    disease_info = disease_info_service.get_info(predicted_class)
    disclaimer = disease_info_service.get_disclaimer()

    probabilities = [
        ClassProbability(class_name=cls, probability=prob)
        for cls, prob in all_probs
    ]

    return PredictionResponse(
        predicted_class=predicted_class,
        confidence=confidence,
        all_probabilities=probabilities,
        disease_info=disease_info,
        warnings=warnings,
        disclaimer=disclaimer,
        is_demo_prediction=is_demo,
    )
