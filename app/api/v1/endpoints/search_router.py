# search_router.py

from fastapi import APIRouter
from app.models.schema import (
    FlightRequest,
    FlightInfo,
    HotelRequest,
    HotelInfo,
    RestaurantRequest,
    RestaurantInfo,
)
from app.service.search_service import SerpAPIService
from app.utils.custom_error import handle_custom_error
from app.utils.parser import (
    parse_flight_results,
    parse_hotel_results,
    parse_restaurant_results,
)

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
            "currency": request.currency,
        }
        query = {k: v for k, v in query.items() if v is not None}

        # Call the flight search service
        result = await SerpAPIService.search_flights(query=query)

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
            "currency": request.currency,
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
