# itinerary_service.py

from datetime import date
from app.models.schema import FlightInfo, HotelInfo, ItineraryResponse
from app.agents.ai_agents import itinerary_agent
from app.utils.custom_error import handle_custom_error
from app.utils.function import clean_json_response
from app.core.logger import get_logger

logger = get_logger(__name__)


# Function to build the context for the itinerary agent
def build_context(destination: str,check_in: date,check_out: date,flight: FlightInfo,hotel: HotelInfo) -> dict:
    return {
        "destination": destination,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "flight_details": (
            f"{flight.airline} ({flight.travel_class}), departs {flight.departure} to {flight.arrival}, "
            f"{flight.duration}, {flight.stops} stops, {flight.price}"
        ),
        "hotel_details": (
            f"{hotel.name} rated {hotel.rating} with amenities: {', '.join(hotel.amenities)}, "
            f"costs {hotel.price_per_night} per night"
        ),
    }

# Function to build the prompt for the itinerary agent
def build_prompt(context: dict) -> str:
    return (
        f"Generate a travel itinerary for a trip to {context['destination']} from "
        f"{context['check_in']} to {context['check_out']}. "
        f"Flight details: {context['flight_details']}. "
        f"Hotel details: {context['hotel_details']}."
    )

# Function to run the itinerary agent with the prompt
def run_itinerary_agent(prompt: str) -> str:
    """Run the itinerary agent with the prompt and return the raw response content."""
    response = itinerary_agent.run(message=prompt)
    return response.content.strip()

# Function to parse the raw AI response into an ItineraryResponse object
def parse_itinerary_response(raw_content: str) -> ItineraryResponse:
    cleaned_content = clean_json_response(raw_content)
    try:
        itinerary = ItineraryResponse.model_validate_json(cleaned_content)
    except Exception as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Problematic JSON: {cleaned_content}")
        raise
    return itinerary

# Function to generate the itinerary plan
async def generate_itinerary_plan(
    destination: str,
    check_in: date,
    check_out: date,
    flight: FlightInfo,
    hotel: HotelInfo,
) -> ItineraryResponse:
    try:
        logger.info(
            f"Generating itinerary plan for {destination} from {check_in} to {check_out}"
        )
        context = build_context(destination, check_in, check_out, flight, hotel)
        prompt = build_prompt(context)
        raw_content = run_itinerary_agent(prompt)
        itinerary = parse_itinerary_response(raw_content)

        return itinerary

    except Exception as e:
        handle_custom_error(e)
