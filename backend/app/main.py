"""FastAPI application entry point."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.exceptions import (
    DiseaseInfoNotFoundError,
    InvalidImageError,
    ModelNotAvailableError,
    disease_info_not_found_handler,
    generic_exception_handler,
    invalid_image_handler,
    model_not_available_handler,
)
from app.services.disease_info import disease_info_service
from app.services.inference import inference_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-assisted coffee leaf disease detection API for Abole. "
    "Classifies coffee leaf images as Healthy, Cercospora, Leaf Rust, Miner, or Phoma. "
    "Predictions are AI-assisted, not confirmed diagnoses.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_exception_handler(InvalidImageError, invalid_image_handler)
app.add_exception_handler(ModelNotAvailableError, model_not_available_handler)
app.add_exception_handler(DiseaseInfoNotFoundError, disease_info_not_found_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Abole Coffee Leaf Disease Detection API...")
    disease_info_service.load()
    inference_service.load_model()
    logger.info(f"Demo mode: {inference_service.is_demo}")
    logger.info(f"Model loaded: {inference_service.model_loaded}")


from app.api.routes import router

app.include_router(router, tags=["Coffee Leaf Disease Detection"])
