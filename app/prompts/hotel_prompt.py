# prompts/hotel_prompt.py

from app.models.schemas import HotelSearchRequest


def build_hotel_prompt(request: HotelSearchRequest) -> str:
    """
    Build a prompt for the hotel recommendation agent using airport code + SerpAPI lookup.

    Args:
        request (HotelSearchRequest): Object containing hotel search input such as:
                    (arrival_id, check_in_date, and check_out_date)

    Returns:
        str: A formatted prompt string that instructs the LLM agent to use SerpAPI's
             Google Hotel engine
    """

    prompt = f"""
    You are part of Trekly, a travel assistant that helps users find the best hotels using SerpAPI's `google_hotels` engine.

    Use the `google_hotels` tool directly with the following inputs:
    - arrival_id: {request.destination}
    - check_in_date: {request.check_in_date}
    - check_out_date: {request.check_out_date}
    - currency: {request.currency or "USD"}

    Step 1:
    Search for hotels using the `google_hotels` tool with the above parameters.

    Step 2:
    From the results, recommend a **top-rated hotel** based on:
    - High rating (4.0+ preferred)
    - Useful amenities (e.g., Wi-Fi, breakfast, restaurant)
    - Good value for price (optional to mention price)

    Step 3:
    Return the response **strictly in the following JSON format**:
    {{
    "recommendation": string,
    "value_explanation": string,
    "hotel_details": {{
        "name": string,
        "image_url": string,
        "price_per_night": string,
        "rating": float,
        "amenities": [string]
    }},
    "source_link": string
    }}

    Recommendation Criteria:
    - Rating: Highlight what the rating suggests about service and cleanliness.
    - Comfort & Amenities: Focus on how well the hotel meets typical travel needs (e.g., Wi-Fi, breakfast, workspace, atmosphere).
    - Price: Mention only if it enhances the value of an already good experience.

    Return ONLY a JSON object with the following keys (no triple backticks):
    """

    return prompt.strip()
