"""Pydantic models for API request/response."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ClassProbability(BaseModel):
    class_name: str = Field(..., description="Disease class name")
    probability: float = Field(..., description="Probability score (0-1)")


class DiseaseInfo(BaseModel):
    name: str
    scientific_name: str
    description: str
    symptoms: List[str]
    management_practices: List[str]
    ethiopian_context: Optional[str] = None
    citations: List[str]


class PredictionResponse(BaseModel):
    predicted_class: str = Field(..., description="Predicted disease class name")
    confidence: float = Field(..., description="Confidence score for top prediction (0-1)")
    all_probabilities: List[ClassProbability] = Field(..., description="All class probabilities sorted by confidence")
    disease_info: DiseaseInfo = Field(..., description="Information about the predicted disease")
    warnings: List[str] = Field(default_factory=list, description="Non-fatal warnings about the input image")
    disclaimer: str = Field(..., description="AI-assisted analysis disclaimer")
    is_demo_prediction: bool = Field(False, description="True if placeholder prediction (no real model loaded)")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    demo_mode: bool
    version: str


class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None
