# agent/hotel_search_service.py

from app.agents.agents import hotel_agent
from app.prompts.hotel_prompt import build_hotel_prompt
from app.utils.validator import validate_hotel_data
from app.models.schemas import HotelSearchRequest
from app.core.exceptions import HotelAgentError, MissingParameterError
from app.utils.request import run_agent_with_retries

# Retruning hotel recommended option
async def get_hotel_options(request: HotelSearchRequest ):
    """
    Run the Hotel recommendation agent using the SerpAPI Google Flights engine.

    Args:
        request (HotelSearchRequest): Hotel search input containing arrival ID, check in date, and check out date.

    Returns:
        Dict: A JSON-compatible dictionary structured

    Raises:
        MissingParameterError: If the prompt is not provided.
        HotelAgentError: If there is an error while retrieving Hotel options.
    """
    # Enuse that all required parameters are present
    if not all([request.destination, request.check_in_date, request.check_out_date]):
        raise MissingParameterError(
            detail="All required hotel parameters must be provided to get a recommendation."
        )

    # Construct the LLM prompt from the passed data
    prompt = build_hotel_prompt(request)

    # Attempt to get hotel recommendation response
    try:
        return  await run_agent_with_retries(
            agent=hotel_agent,
            prompt=prompt,
            validator_fn=validate_hotel_data,
            agent_name="HotelAgent"
        )
    except Exception as e:
        raise HotelAgentError(detail=str(e))
