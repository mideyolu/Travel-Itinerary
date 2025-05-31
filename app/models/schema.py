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
    currency: str = Field("USD", description="Currency for pricing")

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
    currency: str = Field("USD", description="Currency for pricing")


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
    departure: str
    arrival: str

# Hotel Information Schema
class HotelInfo(BaseModel):
    name: str
    image_url: Optional[str] = None  # Hotel image/thumbnail
    price_per_night: str
    rating: Optional[str] = None

# Restaurant Information Schema
class RestaurantInfo(BaseModel):
    title: str
    image_url: Optional[str] = None  # Restaurant image/thumbnail
    rating: Optional[str] = None
    address: str


# Itinerary Request Schema
class ItineraryRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date

    flights: list[FlightInfo]
    hotels: list[HotelInfo]
    restaurants: list[RestaurantInfo]


class ItineraryItem(BaseModel):
    day: int
    date: str
    morning: Optional[str] = None
    afternoon: Optional[str] = None
    evening: Optional[str] = None


# AI Response Schema
class AIResponse(BaseModel):
    destination: str
    start_date: date
    end_date: date
    duration: int  # number of days
    selected_flight: Optional[FlightInfo] = None
    selected_hotel: Optional[HotelInfo] = None
    selected_restaurants: Optional[list[RestaurantInfo]] = None
    itinerary: list[ItineraryItem]


# Itinerary Information Schema
class ItineraryInfo(BaseModel):
    flights: List[FlightInfo]
    hotels: List[HotelInfo]
    resturants: List[RestaurantInfo]
    ai_summary: Optional[str] = Field(None, description="AI-generated summary of the itinerary")
