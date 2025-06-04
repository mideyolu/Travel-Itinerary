# schema.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# -----------------------------
# Request Schemas

# Flight Request Schema
class FlightRequest(BaseModel):
    departure_id: str = Field(
        ..., example="LOS", description="IATA code of the departure airport"
    )
    arrival_id: str = Field(
        ..., example="ABV", description="IATA code of the arrival airport"
    )
    outbound_date: date = Field(..., description="Date of departure")
    return_date: Optional[date] = Field(
        None, description="Date of return (if round trip)"
    )
    # New default fields
    gl: str = Field("ng", description="Google location")


# Hotel Request Schema
class HotelRequest(BaseModel):
    arrival_id: str = Field(
        ...,
        example="ABV",
        description="IATA code of arrival airport (used to determine city)",
    )
    check_in_date: date = Field(..., description="Hotel check-in date")
    check_out_date: date = Field(..., description="Hotel check-out date")
    # New default fields
    gl: str = Field("ng", description="Google location")


# ------------------------------
# Information Response Schema

# Flight Information Schema
class FlightInfo(BaseModel):
    airline: str
    airline_logo: Optional[str] = None  # Airline logo URL
    travel_class: str
    price: str
    duration: str
    stops: int
    departure: str
    arrival: str

# Hotel Information Schema
class HotelInfo(BaseModel):
    name: str
    image_url: Optional[str] = None  # Hotel image/thumbnail
    rating: Optional[str] = None
    amenities: Optional[List[str]] = None  # List of hotel amenities
    essential_info: Optional[str] = None
    price_per_night: Optional[str] = None


# Recommendation Request Schema
class RecommendationRequest(BaseModel):
    flights: List[FlightInfo]
    hotels: List[HotelInfo]

# Recommendation Response Model
class RecommendationResponse(BaseModel):
    ai_flight_recommendation: Optional[dict]
    ai_hotel_recommendation: Optional[dict]



# Itinerary Request Schema
class ItineraryRequest(BaseModel):
    destination: str = Field(
        ..., example="Paris", description="Travel destination city"
    )
    flight: FlightInfo = Field(..., description="Recommended flight option")
    hotel: HotelInfo = Field(..., description="Recommended hotel option")
    check_in_date: date = Field(..., description="Check-in date")
    check_out_date: date = Field(..., description="Check-out date")


class ItineraryActivity(BaseModel):
    time: str
    activity: str

class ItineraryDay(BaseModel):
    day: str
    activities: List[ItineraryActivity]
    restaurant: dict

class ItineraryResponse(BaseModel):
    destination: str
    check_in_date: date
    check_out_date: date
    num_days: str
    daily_plan: List[ItineraryDay]
    transport_tips: str
    flight_info: str
    hotel_info: str
