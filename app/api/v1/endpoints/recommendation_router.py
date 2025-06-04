# recommendation_router.py

from fastapi import APIRouter
from app.models.schema import RecommendationRequest, RecommendationResponse
from app.service.recommendation_service import generate_recommendation
from app.utils.custom_error import handle_custom_error
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/ai/recommendations", response_model=RecommendationResponse)
async def get_ai_recommendations(request: RecommendationRequest):
    try:
        logger.info("Received AI Recommendation Request")

        if not (request.flights or request.hotels):
            logger.error("Flights or Hotels input missing in request")
            return RecommendationResponse(
                ai_flight_recommendation=None, ai_hotel_recommendation=None
            )

        flight_data = await generate_recommendation("flights", request.flights)
        hotel_data = await generate_recommendation("hotels", request.hotels)

        logger.info("AI recommendation generation successful")
        return RecommendationResponse(
            ai_flight_recommendation=flight_data,
            ai_hotel_recommendation=hotel_data,
        )

    except Exception as e:
        logger.error(f"Error in Generating AI Recommendations: {str(e)}")
        handle_custom_error(e)
        return []
