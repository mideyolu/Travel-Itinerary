# ai_agents.py
from agno.agent import Agent
from app.utils.helpers import load_llm


flight_agent = Agent(
    name="Flight Search Recommendation Agent",
    role="Handle flight recommendations based on received data.",
    model=load_llm(),
    description="""
    Based on the flight options provided, recommend the single best flight.
        Return ONLY a JSON object with the following keys:
        {
        "recommendation": string,           # detailed statement of 100 words recommending the flight
        "value_explanation": string,        # Why the price offers the best value compared to others
        "airline_overview": string,         # Brief overview of the airline reputation and features
        "duration_justification": string,   # Why flight duration is optimal including layovers
        "travel_class_benefits": string,    # Benefits of the travel class (comfort, amenities)
        "summary": string,                  # Confident summary reinforcing why this flight is best
        "flight_details": {                 # Key details of the flight
            "airline": string,
            "price": string,
            "departure": string,
            "arrival": string,
            "duration": string,
            "stops": int,
            "travel_class": string
        }
        }
    Do NOT include any text outside the JSON object.
    Provide detailed but clear and concise explanations for each field.
    Here are the flight options:
    {items_dict}

    """,
)


hotel_agent = Agent(
    name="Hotel Search Recommendation Agent",
    role="Handle hotel recommendations based on received data.",
    model=load_llm(),
    description="""
    Based on the hotel options provided, recommend the best hotel.
    Return ONLY a JSON object with the following keys:

    {
      "recommendation": string,          # 50 words clear recommendation naming the hotel
      "value_explanation": string,       # Why this hotel offers the best price-to-quality value
      "rating_analysis": string,         # What the rating implies about service, cleanliness, amenities
      "amenities_highlight": string,     # Standout amenities or essential features
      "summary": string,                 # Summary reinforcing why this hotel is the top choice
      "hotel_details": {                 # Key details of the hotel
        "name": string,
        "price_per_night": string,
        "rating": float,
        "amenities": [string],
        "location": string
      }
    }

    Do NOT include any text outside the JSON object.
    Provide detailed, specific, and clear explanations for each field.
    Here are the hotel options:
    {items_dict}
    """,
)


restaurant_agent = Agent(
    name="Restaurant Search Recommendation Agent",
    role="Handle restaurant recommendations based on received data.",
    model=load_llm(),
    description="""
    From the list of restaurants provided, recommend the best option.
    Return ONLY a JSON object with the following keys:

    {
      "recommendation": string,           # 50 words clear recommendation naming the restaurant
      "value_explanation": string,        # Why this restaurant offers the best value (price/quality)
      "rating_analysis": string,          # What the rating indicates about food and service
      "features": string,                 # Notable features: delivery, atmosphere, parking, etc.
      "operating_hours_fit": string,      # How hours fit typical dining needs
      "summary": string,                  # Summary emphasizing why this is the best choice
      "restaurant_details": {             # Key details of the restaurant
        "name": string,
        "price_range": string,
        "rating": float,
        "cuisine": string,
        "location": string,
        "features": [string]
      }
    }

    Do NOT include any text outside the JSON object.
    Provide detailed and specific explanations for each field.
    Here are the restaurant options:
    {items_dict}
    """,
)
