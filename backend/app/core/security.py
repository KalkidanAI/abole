"""API key authentication dependency for FastAPI."""
from fastapi import Depends, Header, HTTPException, status

from app.config import settings


async def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")) -> str:
    """Verify the X-API-Key header matches the configured API key."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Provide it in the 'X-API-Key' header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return x_api_key
