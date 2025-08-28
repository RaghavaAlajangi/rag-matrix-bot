from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from .config import rag_config

api_key_header = APIKeyHeader(name="X-Internal-Token", auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    """Dependency to get and validate the API key from request headers."""
    if api_key is None or api_key != rag_config.INTERNAL_FASTAPI_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or missing token",
        )
    return api_key
