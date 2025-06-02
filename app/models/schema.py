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


# Restaurant Request Schema
class RestaurantRequest(BaseModel):
    resturant_type: str = Field(
        ..., example="pizza", description="City to search restaurants in"
    )
    latitude: float = Field(..., example=37.7749, description="Latitude of location")
    longitude: float = Field(..., example=-122.4194, description="Longitude of location")


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

# Restaurant Information Schema
class RestaurantInfo(BaseModel):
    title: str
    image_url: Optional[str] = None  # Restaurant image/thumbnail
    address: str
    operating_hours: Optional[str] = None
    extensions: Optional[List[dict]] = None
    rating: Optional[str] = None
    price: Optional[str] = None


# AI Response Schema
class AIResponse(BaseModel):
    flights: Optional[list[FlightInfo]] = None
    hotels: Optional[list[HotelInfo]] = None
    restaurants: Optional[list[RestaurantInfo]] = None
    ai_flight_recommendation: Optional[str] = None
    ai_hotel_recommendation: Optional[str] = None
    ai_resturant_recommendation: Optional[str] = None


# Recommendation Request Schema
class RecommendationRequest(BaseModel):
    flights: List[FlightInfo]
    hotels: List[HotelInfo]
    restaurants: List[RestaurantInfo]

# Recommendation Response Model
class RecommendationResponse(BaseModel):
    ai_flight_recommendation: Optional[str]
    ai_hotel_recommendation: Optional[str]
    ai_restaurant_recommendation: Optional[str]
