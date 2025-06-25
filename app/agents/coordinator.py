import json
from typing import Iterator
from agno.workflow import Workflow, RunEvent, RunResponse
from agno.utils.log import logger

from app.core.exceptions import AgentError
from app.models.schemas import (
    FlightRecommendation,
    HotelRecommendation,
    ItineraryPlan,
    TravelPlanRequest,
)
from app.services.flight_search_service import get_flight_options
from app.services.hotel_search_service import get_hotel_options
from app.agents.itinerary_agent import generate_itinerary


class TravelPlannerWorkflow(Workflow):
    """
    Trekly - Multi-agent workflow orchestrating travel planning

    Agents:
        - FlightAgent: Handles flight search and recommendations.
        - HotelAgent: Handles hotel search and recommendations.
        - ItineraryAgent: Generates a complete travel itinerary based on flight and hotel recommendations.
    """

    description = "Generate a complete travel plan using coordinated agents for flights, hotels, and itinerary."

    def run(
        self, travel_request: TravelPlanRequest, use_cache: bool = True
    ) -> Iterator[RunResponse]:
        logger.info(f"Running TravelPlannerWorkflow with request: {travel_request}")

        # Check for cached result
        if use_cache:
            cached = self.session_state.get("last_plan")
            if cached:
                logger.info("Using cached travel plan.")
                yield RunResponse(
                    content=cached, event=RunEvent.workflow_completed
                )
                return

        try:
            # Run Flight Agent
            logger.info("Running Flight Agent...")
            flight_result = get_flight_options(travel_request.flight_prompt)
            flight_model = FlightRecommendation(**flight_result)

            # Run Hotel Agent
            logger.info("Running Hotel Agent...")
            hotel_result = get_hotel_options(travel_request.hotel_prompt)
            hotel_model = HotelRecommendation(**hotel_result)

            # Build itinerary prompt from details
            itinerary_prompt = f"""
            Destination: {travel_request.destination}
            Dates: {travel_request.check_in_date} to {travel_request.check_out_date}
            Flight Detail: {json.dumps(flight_model.flight_details.model_dump())}
            Hotel Detail: {json.dumps(hotel_model.hotel_details.model_dump())}
            """

            # Run Itinerary Agent
            logger.info("Running Itinerary Agent...")
            itinerary_result = generate_itinerary(itinerary_prompt)
            itinerary_model = ItineraryPlan(**itinerary_result)

            # Final travel plan structure
            plan = {
                "destination": travel_request.destination,
                "flight": flight_model.model_dump(),
                "hotel": hotel_model.model_dump(),
                "itinerary": itinerary_model.model_dump(),
            }

            # Cache result
            self.session_state["last_plan"] = plan
            logger.info("Workflow completed successfully.")

            yield RunResponse(
                content=plan, events=RunEvent.workflow_completed
            )

        except Exception as e:
            logger.error(f"[Workflow] Planning failed: {str(e)}")
            raise AgentError(detail=f"Travel planner failed: {str(e)}")
