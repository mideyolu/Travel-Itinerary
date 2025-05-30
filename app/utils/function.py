# function.py

import httpx
from app.core.config import settings
from app.utils.custom_error import CustomAPIError
import logging

logger = logging.getLogger(__name__)


async def make_serpapi_request(
    engine: str, params: dict = None, error_context: str = "search"
):
    """
    Generic Function to make requests to the SerpAPI service.

    Returns:
        dict: The JSON response from the SerpAPI.

    Raises:
        CustomAPIError: If the request fails or the response is not successful.
    """

    # Always add these params
    params.update({
        "hl": "en",
        "api_key": settings.SERPAPI_API_KEY,
        "engine": engine,
    })

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        logger.error(f"Error during {error_context} request: {str(e)}")
        raise CustomAPIError(details=f"Failed to fetch {error_context} info: {str(e)}")
