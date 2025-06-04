# itinerary_router.py

from fastapi import APIRouter
from app.models.schema import ItineraryRequest, ItineraryResponse
from app.service.itinerary_service import generate_itinerary_plan
from app.utils.custom_error import handle_custom_error
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/ai/itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: ItineraryRequest):
    try:
        logger.info("Received Request for Itinerary Generation")

        if not all(
            [
                request.destination,
                request.flight,
                request.check_in_date,
                request.check_out_date,
                request.hotel,
            ]
        ):
            logger.error("Invalid request data for itinerary generation")
            return ItineraryResponse(itinerary=[])

        itinerary = await generate_itinerary_plan(
            destination=request.destination,
            check_in=request.check_in_date,
            check_out=request.check_out_date,
            flight=request.flight,
            hotel=request.hotel,
        )

        logger.info("AI Itinerary Generation Successful")
        return itinerary

    except Exception as e:
        logger.error(f"Error in Generating Itinerary: {str(e)}")
        handle_custom_error(e)
        return ItineraryResponse(itinerary=[])
