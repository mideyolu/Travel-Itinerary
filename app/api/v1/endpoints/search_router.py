# # search_router.py

# from fastapi import APIRouter
# from app.models.schema import (
#     FlightRequest,
#     FlightInfo,
#     HotelRequest,
#     HotelInfo,
#     RecommendationRequest,
#     RecommendationResponse,
#     ItineraryRequest,
#     ItineraryResponse
# )
# from app.service.search_service import SerpAPIService
# from app.utils.custom_error import handle_custom_error
# from app.utils.parser import (
#     parse_flight_results,
#     parse_hotel_results,
# )
# from app.service.itinerary_service import generate_itinerary_plan
# from app.service.recommendation_service import generate_recommendation
# from app.core.logger import get_logger

# router = APIRouter()
# logger = get_logger(__name__)


# # Endpoint for searching flights
# @router.post("/search/flights", response_model=list[FlightInfo])
# async def search_flights(request: FlightRequest):
#     try:
#         # Logger instance
#         logger.info(f"Received Flight Search Request")

#         # Query for flight search
#         query = {
#             "departure_id": request.departure_id,
#             "arrival_id": request.arrival_id,
#             "outbound_date": request.outbound_date,
#             "return_date": request.return_date,
#             "gl": request.gl,
#         }
#         # Removing null values
#         query = {k: v for k, v in query.items() if v is not None}

#         # Performing search request
#         result = await SerpAPIService.search_flights(query)

#         logger.info("Flight search successful")

#         parsed_result = parse_flight_results(result)

#         # returning parsed flight results
#         return parsed_result

#     except Exception as e:
#         logger.error(f"Error in search_flights: {str(e)}")
#         handle_custom_error(e)
#         return []


# # Endpoint for searching hotels
# @router.post("/search/hotels", response_model=list[HotelInfo])
# async def search_hotels(request: HotelRequest):
#     try:
#         # Logger instance
#         logger.info(f"Received hotel search request")

#         # Query for hotel search
#         query = {
#             "q": request.arrival_id,
#             "check_in_date": str(request.check_in_date),
#             "check_out_date": str(request.check_out_date),
#             "gl": request.gl,
#         }

#         # Removing null values
#         query = {k: v for k, v in query.items() if v is not None}

#         # Performing search request
#         result = await SerpAPIService.search_hotels(query)
#         logger.info("Hotel search successful")

#         parsed_result = parse_hotel_results(result)

#         # Returning parsed hotel results
#         return parsed_result

#     except Exception as e:
#         logger.error(f"Error in search_hotels: {str(e)}")
#         handle_custom_error(e)
#         return []


# # AI Recommendation Endpoint
# @router.post("/ai/recommendations", response_model=RecommendationResponse)
# async def get_ai_recommendations(request: RecommendationRequest):
#     try:
#         logger.info("Received AI Recommendation Request")

#         # Validate request data
#         if not all ([request.flights or not request.hotels]):
#             logger.error("Flights or Hotels input missing in request")
#             return []

#         # Generate recommendations
#         flight_data = await generate_recommendation("flights", request.flights)
#         hotel_data = await generate_recommendation("hotels", request.hotels)

#         logger.info("AI recommendation generation successful")

#         return RecommendationResponse(
#             ai_flight_recommendation=flight_data,
#             ai_hotel_recommendation=hotel_data,
#         )

#     except Exception as e:
#         logger.error(f"Error in Generating AI Recommendations: {str(e)}")
#         handle_custom_error(e)
#         return []

# # Itinerary Endpoint
# @router.post("/ai/itinerary", response_model=ItineraryResponse)
# async def generate_itinerary(request: ItineraryRequest):
#     try:
#         logger.info("Received Request for Itinerrary Generation")

#         # Validate request data
#         if not all ([request.destination, request.flight, request.check_in_date,
#                      request.check_out_date, request.hotel]):

#             logger.error("Invalid request data for itinerary generation")
#             return []

#         # Generate itinerary plan using AI service
#         itinerary = await generate_itinerary_plan(
#             destination=request.destination,
#             check_in=request.check_in_date,
#             check_out=request.check_out_date,
#             flight=request.flight,
#             hotel=request.hotel,
#         )

#         logger.info("AI Itinerary Generation Successful")

#         return itinerary

#     except Exception as e:
#         logger.error(f"Error in Generating Itinerary: {str(e)}")
#         handle_custom_error(e)
#         return []


# app/api/v1/endpoints/search_router.py

from fastapi import APIRouter
from app.models.schema import FlightRequest, FlightInfo, HotelRequest, HotelInfo
from app.service.search_service import SerpAPIService
from app.utils.custom_error import handle_custom_error
from app.utils.parser import parse_flight_results, parse_hotel_results
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/search/flights", response_model=list[FlightInfo])
async def search_flights(request: FlightRequest):
    try:
        logger.info(f"Received Flight Search Request")

        query = {
            "departure_id": request.departure_id,
            "arrival_id": request.arrival_id,
            "outbound_date": request.outbound_date,
            "return_date": request.return_date,
            "gl": request.gl,
        }
        query = {k: v for k, v in query.items() if v is not None}

        result = await SerpAPIService.search_flights(query)
        logger.info("Flight search successful")
        return parse_flight_results(result)

    except Exception as e:
        logger.error(f"Error in search_flights: {str(e)}")
        handle_custom_error(e)
        return []


@router.post("/search/hotels", response_model=list[HotelInfo])
async def search_hotels(request: HotelRequest):
    try:
        logger.info(f"Received Hotel Search Request")

        query = {
            "q": request.arrival_id,
            "check_in_date": str(request.check_in_date),
            "check_out_date": str(request.check_out_date),
            "gl": request.gl,
        }
        query = {k: v for k, v in query.items() if v is not None}

        result = await SerpAPIService.search_hotels(query)
        logger.info("Hotel search successful")
        return parse_hotel_results(result)

    except Exception as e:
        logger.error(f"Error in search_hotels: {str(e)}")
        handle_custom_error(e)
        return []
