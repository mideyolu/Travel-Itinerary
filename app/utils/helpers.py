# utils/helpers.py

from functools import lru_cache
from agno.models.google import Gemini
from app.utils.api_loader import SerpApiTools
from app.core.config import settings
from app.core.exceptions import (
    SerpApiKeyError,
    SerpApiServiceError,
    AgentNotFoundError,
    GeminiApiKeyError,
)
from app.utils.logging import logging


@lru_cache(maxsize=1)
def load_llm():
    """
    Load the Gemini model with the configured API key.

    Returns:
        Gemini: An instance of the Gemini model configured with the API key and model ID.

    Raises:
        GeminiApiKeyError: If the Gemini API key is not set.
        AgentNotFoundError: If the Gemini model could not be loaded.
    """
    if not settings.GEMINI_API_KEY:
        raise GeminiApiKeyError()

    try:
        gemini = Gemini(
            api_key= settings.GEMINI_API_KEY,
            id=settings.MODEL_ID,
            )

        return gemini

    except Exception as e:
        logging.error(f"Error loading Gemini model: {e}")
        raise AgentNotFoundError()


@lru_cache(maxsize=1)
def load_serpapi_tools():
    """
    Load the SerpAPI searvice with the configured API key.

    Returns:
        SerpAPI: An instance of the api service configured with the API key.

    Raises:
        SerpApiKeyError: If the  SerpAPI key is not set.
        SerpApiServiceError: If the SerpAPI service could not be loaded.
    """
    if not settings.SERPAPI_API_KEY:
        raise SerpApiKeyError()

    try:
        return SerpApiTools(api_key=settings.SERPAPI_API_KEY)
    except Exception as e:
        logging.error(f"Error loading SerpApi tools: {e}")
        raise SerpApiServiceError()
