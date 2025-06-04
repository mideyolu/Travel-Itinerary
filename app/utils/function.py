# function.py

import httpx
from app.core.config import settings
from app.utils.custom_error import CustomAPIError
import logging
import re, json
from typing import Optional

logger = logging.getLogger(__name__)


async def make_serpapi_request(
    engine: str, query: dict = None, error_context: str = "search"
):
    """
    Generic Function to make requests to the SerpAPI service.

    Returns:
        dict: The JSON response from the SerpAPI.

    Raises:
        CustomAPIError: If the request fails or the response is not successful.
    """

    # Always add these params
    query.update({
        "hl": "en",
        "api_key": settings.SERPAPI_API_KEY,
        "engine": engine,
        "currency": "USD",

    })

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.BASE_URL}", params=query)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        logger.error(f"Error during {error_context} request: {str(e)}")
        raise CustomAPIError(details=f"Failed to fetch {error_context} info: {str(e)}")


def clean_json_response(text: str) -> str:
    return re.sub(r"^```(?:json)?\n|\n```$", "", text.strip())


def extract_json_from_response(raw_output: str) -> Optional[dict]:
    """Safely extract JSON object from raw string response."""
    try:
        json_str_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if json_str_match:
            json_str = json_str_match.group()
            return json.loads(json_str)
        else:
            logger.error("No JSON found in agent response")
            return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return None
