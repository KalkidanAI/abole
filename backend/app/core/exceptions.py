"""Custom exceptions and exception handlers for the FastAPI app."""
from fastapi import Request
from fastapi.responses import JSONResponse


class InvalidImageError(Exception):
    """Raised when an uploaded file is not a valid or supported image."""
    pass


class ModelNotAvailableError(Exception):
    """Raised when no model is loaded and demo mode is disabled."""
    pass


class DiseaseInfoNotFoundError(Exception):
    """Raised when disease information is not found for a class."""
    pass


async def invalid_image_handler(request: Request, exc: InvalidImageError):
    return JSONResponse(status_code=422, content={"detail": str(exc), "code": "INVALID_IMAGE"})


async def model_not_available_handler(request: Request, exc: ModelNotAvailableError):
    return JSONResponse(status_code=503, content={"detail": str(exc), "code": "MODEL_NOT_AVAILABLE"})


async def disease_info_not_found_handler(request: Request, exc: DiseaseInfoNotFoundError):
    return JSONResponse(status_code=500, content={"detail": str(exc), "code": "DISEASE_INFO_NOT_FOUND"})


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": f"Internal server error: {str(exc)}", "code": "INTERNAL_ERROR"})
