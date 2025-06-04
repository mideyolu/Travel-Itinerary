# search_router.py

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
