# helper.py
from functools import lru_cache
from agno.models.google import Gemini
from app.core.config import settings

# # Helper function to load the LLM
@lru_cache(maxsize=1)
def load_llm():
    """
    Load the LLM (Language Model) with caching to avoid repeated initializations.

    Returns:
        object: The loaded LLM instance.
    """

    return Gemini(
        id="gemini-2.0-flash-lite",
        provider="google",
        api_key=settings.GEMINI_API_KEY,
    )
