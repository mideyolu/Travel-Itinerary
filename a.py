# v1/endpoints.py

from fastapi import APIRouter
from app.models.schemas import (
    FlightSearchRequest,HotelSearchRequest, ItineraryPlanRequest,
    HotelRecommendation,
    FlightRecommendation,
    ItineraryRecommendation,
)
import uuid
from app.agents.coordinator import TravelPlannerWorkflow
from agno.storage.sqlite import SqliteStorage
from app.services.flight_search_service import get_flight_options
from app.services.hotel_search_service import get_hotel_options
from app.services.itinerary_generation_service import generate_itinerary
from app.core.exceptions import ServiceUnavailableError


router = APIRouter()

@router.post("/plan-trip", summary="Generate full travel itinerary")
def plan_trip(payload: ItineraryPlanRequest):
    # """
    # Run the multi-agent workflow to generate flights, hotels, and itinerary.

    # Args:
    #     payload (TravelPlanInput): User input including destination, dates, and agent prompts.

    # Returns:
    #     dict: Combined JSON result from all agents.
    # """
    # try:
    #     session_id = f"trip-{uuid()}"
    #     planner = TravelPlannerWorkflow(
    #         session_id=session_id,
    #         storage=SqliteStorage(
    #             table_name="travel_workflows", db_file="tmp/travel_workflow.db"
    #         ),
    #         debug_mode=True,
    #     )

    #     result = next(planner.run(travel_request=payload))
    #     return result.content

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    pass


@router.post("/search-flight", response_model=FlightRecommendation)
async def search_flight(payload: FlightSearchRequest):
    try:
        result = get_flight_options(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))


@router.post("/search-hotel", response_model=HotelRecommendation)
def search_hotel(payload: HotelSearchRequest):
    try:
        result = get_hotel_options(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))


@router.post("/generate-itinerary", response_model=ItineraryRecommendation)
def generate_itinerary_plan(payload: ItineraryPlanRequest):
    try:
        result = generate_itinerary(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))
