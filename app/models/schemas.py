# models/schem.py

from pydantic import BaseModel
from typing import List, Optional
from app.models.itinerary_schemas import DayPlan

# Request Model
class FlightSearchRequest(BaseModel):
    """Model for flight search request"""
    departure_id: str
    arrival_id: str
    outbound_date: str
    return_date: Optional[str] = None
    currency: Optional[str] = "USD"

class HotelSearchRequest(BaseModel):
    """Model for hotel search request."""
    arrival_id: str
    check_in_date: str
    check_out_date: str
    currency: Optional[str] = "USD"

class ItineraryPlanRequest(BaseModel):
    """Model for itineray travel plan request."""
    destination: str
    check_in_date: str
    check_out_date: str

# Response Model
class FlightDetails(BaseModel):
    """Model for flight option response."""
    airline: str
    airline_logo: Optional[str] = None
    travel_class: str
    price: str
    duration: str
    departure_time: str
    arrival_time: str

class HotelDetails(BaseModel):
    """Model for hotel option response."""
    name: str
    image_url: Optional[str] = None
    rating: Optional[float] = None
    amenities: Optional[List[str]] = None
    price_per_night: Optional[str] = None

class ItineraryDetails(BaseModel):
    """Model for itinerary response."""
    destination: str
    num_days: str
    daily_plan: List[DayPlan]
    check_in_date: str
    check_out_date: str

# Recommendation
class FlightRecommendation(BaseModel):
    recommendation: str
    value_explanation: str
    flight_details: FlightDetails
    source_link: Optional[str] = None

class HotelRecommendation(BaseModel):
    recommendation: str
    value_explanation: str
    hotel_details: HotelDetails
    source_link: Optional[str] = None

class ItineraryRecommendation(BaseModel):
    itinerary_details: ItineraryDetails
    transport_tips: str
    expectation: str
