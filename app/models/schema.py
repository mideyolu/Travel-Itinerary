#schema.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

#-----------------------------
# Request Schemas

# Flight Request Schema
class FlightRequest(BaseModel):
    departure_airport: str = Field(
        ..., example="LOS", description="IATA code of the departure airport"
    )
    arrival_airport: str = Field(
        ..., example="ABV", description="IATA code of the arrival airport"
    )
    departure_date: date = Field(..., description="Date of departure")
    return_date: Optional[date] = Field(
        None, description="Date of return (if round trip)"
    )

# Hotel Request Schema
class HotelRequest(BaseModel):
    arrival_airport: str = Field(
        ...,
        example="ABV",
        description="IATA code of arrival airport (used to determine city)",
    )
    check_in_date: date = Field(..., description="Hotel check-in date")
    check_out_date: date = Field(..., description="Hotel check-out date")


# Restaurant Request Schema
class RestaurantRequest(BaseModel):
    destination_city: str = Field(
        ..., example="Abuja", description="City to search restaurants in"
    )

# Itinerary Request Schema
class ItineraryRequest(BaseModel):
    flight: FlightRequest
    hotel: HotelRequest
    restaurant: RestaurantRequest


#------------------------------
# Information Response Schema

# Flight Information Schema
class FlightInfo(BaseModel):
    airline: str
    logo_url: Optional[str] = None  # Airline logo URL
    price: str
    duration: str
    departure_time: str
    arrival_time: str

# Hotel Information Schema
class HotelInfo(BaseModel):
    name: str
    image_url: Optional[str] = None  # Hotel image/thumbnail
    price_per_night: str
    address: str
    rating: Optional[str] = None

# Restaurant Information Schema
class RestaurantInfo(BaseModel):
    name: str
    image_url: Optional[str] = None  # Restaurant image/thumbnail
    rating: Optional[str] = None
    cuisine: Optional[str] = None
    address: str

# Itinerary Information Schema
class ItineraryInfo(BaseModel):
    flights: List[FlightInfo]
    hotels: List[HotelInfo]
    resturants: List[RestaurantInfo]
    ai_summary: Optional[str] = Field(None, description="AI-generated summary of the itinerary")
