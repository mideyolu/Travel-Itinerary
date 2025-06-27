# prompts/itinerary_prompt.py

from app.models.schemas import ItineraryPlanRequest


def build_itinerary_prompt(request: ItineraryPlanRequest) -> str:
    """
    Build a prompt for the itinerary generation agent using destination, check-in and check-out dates,
    with support from the `search_google` tool for location enrichment and itinerary generation.

    Args:
        request (TravelPlanRequest): Object containing itinerary input: (destination (airport code or location), check_in_date, check_out_date)

    Returns:
        str: A structured prompt string instructing the LLM agent to generate a multi-day travel itinerary.
    """

    prompt = f"""
        You are a part of Trekly — a travel assistant that uses the `search_google` tool for destination lookup and planning support.

        You are tasked to generate a detailed day-by-day travel itinerary using the following user input:

        - Destination: `{request.destination}` (Note: this may be an airport code — resolve it using `search_google`)
        - Check-in Date: `{request.check_in_date}`
        - Check-out Date: `{request.check_out_date}`

        ---
        Instructions:

        Step 1 — Destination Resolution: Use `search_google` to resolve the destination (e.g., airport code like `CDG`) to a full city and country name (e.g., Paris, France).

        Step 2 — Itinerary Planning:
        Using the resolved destination, generate a multi-day itinerary.
        - Determine the number of days by calculating the difference between `check_out_date` and `check_in_date`.
        - Create 1 daily plan per day.
        - Each day's plan must include 2-4 key activities spaced out through the day.
        - Include one restaurant recommendation per day with cuisine type and a tip.

        Step 3 — Quality Check:
        Choose only tourist-friendly, popular, and local-highlight experiences.
        Use your tool access to confirm cultural spots, experiences, and must-visit attractions.
        ---

        Your response should strictly follow this JSON format:
        {{
        "itinerary_details": {{
                "destination": "Paris, France",
                "check_in_date": "2025-07-01",
                "check_out_date": "2025-07-05",
                "num_days": "4",
                "daily_plan": [
                {{
                    "day": "Day 1",
                    "activities": [
                    {{ "time": "09:00 AM", "activity": "Visit the Eiffel Tower" }},
                    {{ "time": "12:00 PM", "activity": "Lunch at a local café" }},
                    {{ "time": "03:00 PM", "activity": "Walk along the Seine River" }}
                    ],
                    "restaurant": {{
                    "name": "Le Relais de l'Entrecôte",
                    "cuisine": "French",
                    "tip": "Try the steak-frites with their secret sauce."
                    }}
                }}
                // Add more days...
                ],
                "transport_tips": "Use Uber or the Paris Metro for quick local travel.",
                "expectation": "A well-rounded experience of Parisian culture, cuisine, and iconic attractions."
        }}
        }}

    """

    return prompt.strip()
