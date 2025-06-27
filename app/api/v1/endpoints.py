# v1/endpoints.py

from fastapi import APIRouter, HTTPException
from app.models.schemas import TripPlanRequest, TripPlanRecommendation
from app.core.exceptions import BaseAppException
from app.agents.coordinator import TreklyTravelPlanner


router = APIRouter()

# Travel Planner Search and Recommendation Endpoint
@router.post("/plan-trip", response_model=TripPlanRecommendation)
async def plan_trip(requests: TripPlanRequest):
    """
    Endpoint to generate a full travel plan including flight, hotel, and itinerary.

    Args:
        requests (TripPlanRequest): User input including departure_id, arrival_id, destination, check-in, check-out dates and the likes.

    Returns:
        TripPlanRecommendation: A structured response containing the recommended flight, hotel, and complete itinerary details.
    """

    try:
        planner = TreklyTravelPlanner()
        result = await planner.execute(requests)
        return result

    except BaseAppException as e:
        raise HTTPException(status_code=500, detail=str(e))
