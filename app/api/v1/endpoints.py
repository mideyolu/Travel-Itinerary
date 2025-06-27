# v1/endpoints.py

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    FlightSearchRequest, HotelSearchRequest,
    ItineraryPlanRequest, HotelRecommendation,
    FlightRecommendation, ItineraryRecommendation,
    TripPlanRequest, TripPlanRecommendation )
import uuid
from app.services.flight_search_service import get_flight_options
from app.services.hotel_search_service import get_hotel_options
from app.services.itinerary_generation_service import generate_itinerary
from app.core.exceptions import ServiceUnavailableError, BaseAppException
from app.agents.coordinator import TreklyTravelPlanner


router = APIRouter()

# Flight Search and Recommendation Endpoint
@router.post("/search-flight", response_model=FlightRecommendation)
async def search_flight(payload: FlightSearchRequest):
    """
    Endpoint to search for flights based on user input.

    Args:
      payload (FlightSearchRequest): User input including departure and arrival IDs, dates, and currency.

    Returns:
       FlightRecommendation: A structured response containing flight option and details.
    """
    try:
        result =  await get_flight_options(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))

# Hotel Search and Recommendation Endpoint
@router.post("/search-hotel", response_model=HotelRecommendation)
async def search_hotel(payload: HotelSearchRequest):
    """
    Endpoint to search for hotels based on user input.

    Args:
        payload (HotelSearchRequest): User input including arrival ID, check-in and check-out dates, and currency.

    Returns:
        HotelRecommendation: A structured response containing hotel option and details.
    """
    try:
        result = await get_hotel_options(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))

# Itinerary Generation Endpoint
@router.post("/generate-itinerary", response_model=ItineraryRecommendation)
async def generate_itinerary_plan(payload: ItineraryPlanRequest):
    """
    Endpoint to generate a complete travel itinerary based on flight and hotel recommendations.

    Args:
        payload (ItineraryPlanRequest): User input including destination, check-in and check-out dates.

    Returns:
        ItineraryRecommendation: A structured response containing the complete itinerary details.
    """
    try:
        result = await generate_itinerary(payload)
        return result
    except Exception as e:
        raise ServiceUnavailableError(detail=str(e))


@router.post("/plan-trip", response_model=TripPlanRecommendation)
async def plan_trip(requests: TripPlanRequest):
    """
    Endpoint to generate a full travel plan including flight, hotel, and itinerary.
    """

    try:
        planner = TreklyTravelPlanner()
        result = await planner.execute(requests)
        return result

    except BaseAppException as e:
        raise HTTPException(status_code=500, detail=str(e))
