# search_router.py

from fastapi import APIRouter
from app.models.schema import (
    FlightRequest,
    FlightInfo,
    HotelRequest,
    HotelInfo,
    RestaurantRequest,
    RestaurantInfo,
    RecommendationRequest,
    RecommendationResponse,
)
from app.service.search_service import SerpAPIService
from app.utils.custom_error import handle_custom_error
from app.utils.parser import (
    parse_flight_results,
    parse_hotel_results,
    parse_restaurant_results,
)
from app.service.ai_service import generate_recommendation
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


# Endpoint for searching flights
@router.post("/search/flights", response_model=list[FlightInfo])
async def search_flights(request: FlightRequest):
    try:
        # Logger instance
        logger.info(f"Received Flight Search Request")

        # Query for flight search
        query = {
            "departure_id": request.departure_id,
            "arrival_id": request.arrival_id,
            "outbound_date": request.outbound_date,
            "return_date": request.return_date,
            "gl": request.gl,
        }
        # Removing null values
        query = {k: v for k, v in query.items() if v is not None}

        # Performing search request
        result = await SerpAPIService.search_flights(query)

        logger.info("Flight search successful")

        parsed_result = parse_flight_results(result)

        # returning parsed flight results
        return parsed_result

    except Exception as e:
        logger.error(f"Error in search_flights: {str(e)}")
        handle_custom_error(e)
        return []


# Endpoint for searching hotels
@router.post("/search/hotels", response_model=list[HotelInfo])
async def search_hotels(request: HotelRequest):
    try:
        # Logger instance
        logger.info(f"Received hotel search request")

        # Query for hotel search
        query = {
            "q": request.arrival_id,
            "check_in_date": str(request.check_in_date),
            "check_out_date": str(request.check_out_date),
            "gl": request.gl,
        }

        # Removing null values
        query = {k: v for k, v in query.items() if v is not None}

        # Performing search request
        result = await SerpAPIService.search_hotels(query)
        logger.info("Hotel search successful")

        parsed_result = parse_hotel_results(result)

        # Returning parsed hotel results
        return parsed_result

    except Exception as e:
        logger.error(f"Error in search_hotels: {str(e)}")
        handle_custom_error(e)
        return []


# Endpoint for searching restaurants
@router.post("/search/restaurants", response_model=list[RestaurantInfo])
async def search_restaurants(request: RestaurantRequest):
    try:

        # Logger instance
        logger.info(f"Received restaurant search request")

        # Query for restaurant search
        query = {
            "q": request.resturant_type,
            "ll": f"@{request.latitude},{request.longitude},1z",
        }

        # Removing null values
        query = {k: v for k, v in query.items() if v is not None}

        # Performing search request
        result = await SerpAPIService.search_restaurants(query)

        logger.info("Restaurant search successful")

        parsed_result = parse_restaurant_results(result)

        # Returning parsed restaurant results
        return parsed_result

    except Exception as e:
        logger.error(f"Error in search_restaurants: {str(e)}")
        handle_custom_error(e)
        return []


# AI Recommendation Endpoint
@router.post("/recommendations", response_model=RecommendationResponse)
async def get_ai_recommendations(request: RecommendationRequest):
    try:
        # Logger instance
        logger.info(f"Received AI recommendation request")

        # Generating AI Recommendations
        flight_data = await generate_recommendation("flights", request.flights)

        hotel_data = await generate_recommendation("hotels", request.hotels)

        restaurant_data = await generate_recommendation("restaurants", request.restaurants)

        logger.info("AI recommendation generation successful")


        # Returning AI Responses
        return RecommendationResponse(
            ai_flight_recommendation=flight_data,
            ai_hotel_recommendation=hotel_data,
            ai_restaurant_recommendation=restaurant_data,
        )

    except Exception as e:
        logger.error(f"Error in get_ai_recommendations: {str(e)}")
        handle_custom_error(e)
        return RecommendationResponse(
            ai_flight_recommendation=None,
            ai_hotel_recommendation=None,
            ai_restaurant_recommendation=None,
        )
