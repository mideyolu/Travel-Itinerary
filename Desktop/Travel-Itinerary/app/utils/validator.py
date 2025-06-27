# utils/validator.py

from typing import List
from app.core.exceptions import MissingParameterError

# Required fields
REQUIRED_FLIGHT_FIELDS = [
    "airline",
    "price",
    "departure",
    "arrival",
    "duration",
    "travel_class",
]

REQUIRED_HOTEL_FIELDS = ["name", "image_url", "rating", "amenities", "price_per_night"]

REQUIRED_ITINERARY_FIELDS =[
    "destination", "num_days", "transport_tips", "daily_plan", "check_in_date","check_out_date"
]

def validate_required_fields(
    data: dict, parent_key: str, required_fields: List[str]
) -> bool:
    """
    Generic validator for checking required fields under a specific parent key.

    Args:
        data (dict): The data to validate.
        parent_key (str): Key where target fields are nested.
        required_fields (List[str]): List of required field names.

    Returns:
        bool: True if all required fields are present and non-empty, False otherwise.
    """
    try:
        section = data.get(parent_key, {})
        return all(section.get(field) for field in required_fields)
    except Exception as e:
        raise MissingParameterError(detail=f"Validation error: {str(e)}")


def validate_flight_data(data: dict) -> bool:
    """Validate flight response."""
    return validate_required_fields(data, "flight_details", REQUIRED_FLIGHT_FIELDS)


def validate_hotel_data(data: dict) -> bool:
    """Validate hotel response."""
    return validate_required_fields(data, "hotel_details", REQUIRED_HOTEL_FIELDS)

def validate_itinerary_data(data: dict) -> bool:
    """Validate itinerary response."""

    try:
        # Ensure the main itinerary_details section is present
        if not validate_required_fields(data, "itinerary_details", REQUIRED_ITINERARY_FIELDS):
            return False

        # Get the itinerary details section
        itinerary = data.get("itinerary_details", {})

        # Check if daily_plan is a list and not empty
        for day in itinerary.get("daily_plan", []):
            if not day.get("activities") or not day.get("restaurant"):
                return False

        return True

    except Exception as e:
        raise MissingParameterError(detail=f"Validation error: {str(e)}")
