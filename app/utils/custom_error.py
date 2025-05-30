# custom_error.py

from fastapi import HTTPException
import logging

# logger configuration
logger = logging.getLogger(__name__)


# Custom exception for API errors
class CustomAPIError(Exception):
    def __init__(self, details: str, status_code: int = 400):
        self.details = details
        self.status_code = status_code


def handle_custom_error(err: Exception):
    logger.error(f"Custom API Error: {str(err)}")

    if isinstance(err, CustomAPIError):
        raise HTTPException(status_code=err.status_code, detail=err.details)

    # For other unexpected exceptions
    raise HTTPException(status_code=500, detail="Internal server error")
