# services/itinerary_generation_service.py

from app.agents.agents import itinerary_agent
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.utils.validator import validate_itinerary_data
from app.models.schemas import ItineraryPlanRequest
from app.core.exceptions import ItineraryPlannerAgentError, MissingParameterError
from app.utils.request import run_agent_with_retries


async def generate_itinerary(request: ItineraryPlanRequest):
    """
        Run the itinerary generation agent using the SerpAPI Google Search engine.

        Args:
            request (ItineraryPlanRequest): Itinerary plan request containing user preferences,
                                            destinations, check in and check out dates.

        Returns:
            Dict: A JSON-compatible dictionary structured.

        Raises:
            MissingParameterError: If the prompt is not provided.
            ItineraryPlannerAgentError: If the agent fails after multiple attempts to return valid flight data.
    """

    # Ensure that all required parameters are present
    if not all([request.destination, request.check_in_date, request.check_out_date]):
        raise MissingParameterError(
            detail="All required itinerary parameters must be provided to get a recommendation."
        )

    # Construct the LLM prompt from the passed data
    prompt = build_itinerary_prompt(request)

    # Attempt to get flight recommendation response
    try:
        return await run_agent_with_retries(
            agent=itinerary_agent,
            prompt=prompt,
            validator_fn=validate_itinerary_data,
            agent_name="Itinerary Planner Agent"
        )
    except Exception as e:
        raise ItineraryPlannerAgentError(detail=str(e))
