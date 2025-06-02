# parser.py
import json
import re
from app.models.schema import FlightInfo, HotelInfo, RestaurantInfo


def parse_flight_results(result: dict) -> list[FlightInfo]:
    """Extracts and returns the top 5 flight results sorted by appearance."""
    flights = []

    for group in result.get("other_flights", []):
        if not group.get("flights"):
            continue  # Skip groups with no flight data

        flight = group["flights"][0]  # Take the first flight in the group

        flights.append(
            FlightInfo(
                airline=flight.get("airline", "Unknown"),
                airline_logo=flight.get("airline_logo") or group.get("airline_logo"),
                travel_class=flight.get("travel_class", "N/A"),
                price=str(group.get("price", "N/A")) + "USD",
                stops=flight.get("stops", 0),
                duration=str(group.get("total_duration", "N/A")) + " minutes",
                departure=flight.get("departure_airport", {}).get("time", "N/A"),
                arrival=flight.get("arrival_airport", {}).get("time", "N/A"),
            )
        )

    return flights


def parse_hotel_results(result: dict) -> list[HotelInfo]:
    """Extracts and returns the top 5 hotels sorted by overall rating."""
    hotels = []

    hotels_data = result.get("properties", [])

    # Sort hotels by rating in descending order
    hotels_data.sort(key=lambda x: float(x.get("overall_rating") or 0), reverse=True)

    for prop in hotels_data:
        name = prop.get("name", "Unknown Hotel")
        images = prop.get("images", [])
        image_url = (
            images[0]["thumbnail"] if images else None
        )  # Use the first image thumbnail
        rate_info = prop.get("rate_per_night", {})
        price_per_night = rate_info.get("lowest", "N/A")
        rating = str(prop.get("overall_rating", "N/A")) + " ⭐"
        amenities = prop.get("amenities", [])
        essential_info = str(prop.get("essential_info", "N/A"))

        hotels.append(
            HotelInfo(
                name=name,
                image_url=image_url,
                price_per_night=price_per_night,
                rating=rating,
                amenities=amenities,
                essential_info=essential_info,
            )
        )

    return hotels


def parse_restaurant_results(result: dict) -> list[RestaurantInfo]:
    """Extracts and returns the top 5 restaurants sorted by rating."""
    restaurants = result.get("local_results", [])

    # Sort restaurants by rating in descending order
    restaurants.sort(key=lambda r: float(r.get("rating") or 0), reverse=True)

    return [
        RestaurantInfo(
            title=restaurant.get("title", "Unknown"),
            image_url=restaurant.get("thumbnail", None),
            address=restaurant.get("address", "N/A") or restaurant.get("photo", None),
            operating_hours=str(restaurant.get("operating_hours", "N/A")),
            extensions=restaurant.get("extensions", {}),
            rating=str(restaurant.get("rating", "N/A")) + " ⭐",
            price=str(restaurant.get("price", "N/A")),
        )
        for restaurant in restaurants
    ]

def parse_json_from_ai_output(output: str) -> dict:
    """
    Extracts and parses JSON from an AI model output string.
    Handles markdown code blocks and plain JSON strings.
    """
    # Try extracting JSON from code block
    match = re.search(r"```(?:json)?\s*({.*?})\s*```", output, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = output.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError("AI output is not valid JSON")
