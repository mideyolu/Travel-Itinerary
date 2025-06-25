# models/schem.py

from pydantic import BaseModel
from typing import List, Optional

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

class TravelPlanRequest(BaseModel):
    """Model for travel plan request."""
    destination: str
    duration: int
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

# Itineray plan generic schemas
# Resturant
class Resturant(BaseModel):
    """Model for restaurant details."""
    name: str
    cuisine: str

# Activity
class Activity(BaseModel):
    """Model for activity details."""
    time: str
    activity: str

# Day Plan
class DayPlan(BaseModel):
    """Model for daily itinerary plan."""
    day: str
    activities: List[Activity]
    restaurant: Resturant

class ItineraryRequest(BaseModel):
    """Model for itinerary request."""
    origin: str
    destination: str
    departure_date: str
    return_date: str

class ItineraryPlan(BaseModel):
    """Model for itinerary response."""
    destination: str
    daily_plan: List[DayPlan]
    num_days: str
    transport_tips: str
    flight_info: str
    hotel_info: str
    check_in_date: str
    check_out_date: str
    destination: str
