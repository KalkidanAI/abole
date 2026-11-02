"""FastAPI dependencies."""
from fastapi import Depends

from app.core.security import verify_api_key
from app.services.disease_info import disease_info_service
from app.services.inference import inference_service
from app.services.preprocessing import preprocessing_service


def get_preprocessing_service():
    return preprocessing_service


def get_inference_service():
    return inference_service


def get_disease_info_service():
    return disease_info_service


api_key_dependency = Depends(verify_api_key)
