# agent/flight_search_service.py

from app.agents.flight_agent import flight_agent
from app.prompts.flight_prompt import build_flight_prompt
from app.utils.validator import validate_flight_data
from app.models.schemas import FlightSearchRequest
from app.core.exceptions import FlightAgentError, MissingParameterError
from app.utils.request import run_agent_with_retries


# Retruning flight recommended option
def get_flight_options(request: FlightSearchRequest):
    """
    Run the flight recommendation agent using the SerpAPI Google Flights engine.

    Args:
        request (FlightSearchRequest): Flight search input containing departure ID, arrival ID,
                                       outbound date, return date (optional), and currency (optional).

    Returns:
        Dict: A JSON-compatible dictionary structured.

    Raises:
        MissingParameterError: If the prompt is not provided.
        FlightAgentError: If the agent fails after multiple attempts to return valid flight data.
    """

    # Enuse that all required parameters are present
    if not all([request.departure_id, request.arrival_id, request.outbound_date]):
        raise MissingParameterError(
            detail="All required flight parameters must be provided to get a recommendation."
        )

    # Construct the LLM prompt from the passed data
    prompt = build_flight_prompt(request)

    # Attempt to get flight recommendation response
    try:
        return run_agent_with_retries(
            agent=flight_agent,
            prompt=prompt,
            validator_fn=validate_flight_data,
            agent_name="FlightAgent"
        )
    except Exception as e:
        raise FlightAgentError(detail=str(e))
