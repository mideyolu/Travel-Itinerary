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

router = APIRouter()


# Endpoint for searching flights
@router.post("/search/flights", response_model=list[FlightInfo])
async def search_flights(request: FlightRequest):
    try:
        # Construct the query from request data, excluding None values
        query = {
            "departure_id": request.departure_id,
            "arrival_id": request.arrival_id,
            "outbound_date": request.outbound_date,
            "return_date": request.return_date,
            "gl": request.gl,  # Geo location
            }
        query = {k: v for k, v in query.items() if v is not None}

        # Call the flight search service
        result = await SerpAPIService.search_flights(query)

        # Parse and return top 5 flight results
        return parse_flight_results(result)

    except Exception as e:
        # Handle and log the error
        handle_custom_error(e)
        return []


# Endpoint for searching hotels
@router.post("/search/hotels", response_model=list[HotelInfo])
async def search_hotels(request: HotelRequest):
    try:
        # Construct the hotel search query
        query = {
            "q": request.arrival_id,  # Search location ( for destination airport)
            "check_in_date": str(request.check_in_date),
            "check_out_date": str(request.check_out_date),
            "gl": request.gl,
        }
        query = {k: v for k, v in query.items() if v is not None}

        # Call the hotel search service
        result = await SerpAPIService.search_hotels(query)

        # Parse and return top 5 hotel results
        return parse_hotel_results(result)

    except Exception as e:
        # Handle and log the error
        handle_custom_error(e)
        return []


# Endpoint for searching restaurants
@router.post("/search/restaurants", response_model=list[RestaurantInfo])
async def search_restaurants(request: RestaurantRequest):
    try:
        # Construct the restaurant search query
        query = {
            "q": request.resturant_type,
            "ll": f"@{request.latitude},{request.longitude},1z",  # Location format for SERP API
        }
        query = {k: v for k, v in query.items() if v is not None}

        # Call the restaurant search service
        result = await SerpAPIService.search_restaurants(query)

        # Parse and return top 5 restaurant results
        return parse_restaurant_results(result)

    except Exception as e:
        # Handle and log the error
        handle_custom_error(e)
        return []


# -- AI Recommendation Endpoint
@router.post("/recommendations", response_model=RecommendationResponse)
async def get_ai_recommendations(request: RecommendationRequest):
    try:
        flight_data = await generate_recommendation("flights", request.flights)
        hotel_data = await generate_recommendation("hotels", request.hotels)
        restaurant_data = await generate_recommendation("restaurants", request.restaurants)


        result = RecommendationResponse(
            ai_flight_recommendation=flight_data,
            ai_hotel_recommendation=hotel_data,
            ai_restaurant_recommendation=restaurant_data
        )
        print(result.json())
        return result

    except Exception as e:
        handle_custom_error(e)
        return RecommendationResponse(
            ai_flight_recommendation="Failed to generate flight recommendation.",
            ai_hotel_recommendation="Failed to generate hotel recommendation.",
            ai_restaurant_recommendation="Failed to generate restaurant recommendation.",
        )
