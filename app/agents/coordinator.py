# agents/coordinator.py

from agno.workflow import Workflow
from app.models.schemas import TripPlanRequest, TripPlanRecommendation
from app.services.flight_search_service import get_flight_options
from app.services.hotel_search_service import get_hotel_options
from app.services.itinerary_generation_service import generate_itinerary
from app.utils.logging import logging
from app.core.exceptions import (
    FlightAgentError,
    HotelAgentError,
    ItineraryPlannerAgentError,
    MissingParameterError,
)
from app.agents.planner import fill_missing_fields, execute_agent


class TreklyTravelPlanner(Workflow):
    """
    TreklyTravelPlanner orchestrates the entire trip planning process
    by coordinating flight, hotel, and itinerary recommendation agents.
    """

    async def execute(self, request: TripPlanRequest) -> TripPlanRecommendation:
        """
        Full Travel Workflow.

        Args:
            request (TripPlanRequest): User's input containing flight, hotel, and itinerary fields.

        Returns:
            TripPlanRecommendation: Final combined recommendation output from all three agents.
        """
        logging.info("🚀 Trekly Travel Planner Workflow Started")

        if not request.flights:
            raise MissingParameterError("Flight details are required.")

        # Flight
        flight_result = await execute_agent(
            "Flight", get_flight_options, request.flights, FlightAgentError
        )

        # Hotel
        logging.info("Auto-filling Hotel fields from Flight...")
        fill_missing_fields(request.hotels, request.flights)
        hotel_result = await execute_agent(
            "Hotel", get_hotel_options, request.hotels, HotelAgentError
        )

        # Itinerary
        logging.info("Auto-filling Itinerary fields from Hotel or Flight...")
        fill_missing_fields(request.itineraries, request.hotels, prefer_dates_from=request.flights)
        itinerary_result = await execute_agent(
            "Itinerary",
            generate_itinerary,
            request.itineraries,
            ItineraryPlannerAgentError,
        )

        logging.info("Trekly Travel Planner Workflow Complete")

        return TripPlanRecommendation(
            flight=flight_result,
            hotel=hotel_result,
            itinerary=itinerary_result,
        )
