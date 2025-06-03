# ai_agents.py

from agno.agent import Agent
from app.utils.helpers import load_llm

# Load the llm once
llm_model = load_llm()

# Flight Recommendation Agent
flight_agent = Agent(
    name="Flight Search Recommendation Agent",
    role="Handle flight recommendations based on received data.",
    model=llm_model,
    description="""
    Based on the flight options provided, recommend the single best flight by considering overall traveler experience and practicality.

    **Reasoning for Recommendation:**
    - **Overall Comfort:** Consider factors like travel class, and duration that impact the passenger’s experience.
    - **Convenience:** Evaluate timing (departure/arrival), and total duration in terms of travel ease.
    - **Stops:** Fewer stops are typically preferred, but explain if a multi-stop option is justified.
    - **Travel Class:** Explain why the comfort and benefits of the travel class stand out.
    - **Price:** Mention value only if it contributes meaningfully to the overall recommendation—don't prioritize it above comfort and convenience.

    Return ONLY a JSON object with the following keys (no triple backticks):

    {
    "recommendation": string,          // A 100-word detailed recommendation justifying the selected flight
    "value_explanation": string,       // Explanation that focuses on comfort, timing, convenience, with price only if relevant
    "flight_details": {
        "airline": string,
        "price": string,
        "departure": string,
        "arrival": string,
        "duration": string,
        "stops": int,
        "travel_class": string
    }
    }

    Be holistic and user-focused in your explanation.
    Here are the flight options:
    {items_dict}
    """,
)

# Hotel Recommendation Agent
hotel_agent = Agent(
    name="Hotel Search Recommendation Agent",
    role="Handle hotel recommendations based on received data.",
    model=llm_model,
    description="""
    Based on the hotel options provided, recommend the most suitable hotel considering quality, comfort, and user experience.

    **Reasoning for Recommendation:**
    - **Rating:** Highlight what the rating suggests about service and cleanliness.
    - **Comfort & Amenities:** Focus on how well the hotel meets typical travel needs (e.g., Wi-Fi, breakfast, workspace, atmosphere).
    - **Price:** Mention only if it enhances the value of an already good experience.

    Return ONLY a JSON object with the following keys (no triple backticks):

    {
    "recommendation": string,          // 100-word balanced recommendation naming the hotel
    "value_explanation": string,       // Explanation focusing on quality, location, and comfort (not price-centric)
    "hotel_details": {
        "name": string,
        "price_per_night": string,
        "rating": float,
        "amenities": [string]
    }
    }

    Be balanced and focused on guest satisfaction.
    Here are the hotel options:
    {items_dict}
    """,
)

# Restaurant Recommendation Agent
restaurant_agent = Agent(
    name="Restaurant Search Recommendation Agent",
    role="Handle restaurant recommendations based on received data.",
    model=llm_model,
    description="""
    From the list of restaurants provided, recommend the one that offers the best dining experience overall.

    **Reasoning for Recommendation:**
    - **Rating:** Emphasize the quality of food and service based on ratings and reviews.
    - **Cuisine & Ambience:** Consider the uniqueness or suitability of cuisine type and atmosphere.
    - **Dining Features:** Look at accessibility, service options, dining style, and special features like outdoor seating, kid-friendliness, etc.
    - **Hours:** Make sure it aligns with common dining times or user needs.
    - **Price:** Only factor in price if it adds to a great experience—not as the primary decision maker.

    Return ONLY a JSON object with the following keys (no triple backticks):

    {
    "recommendation": string,           // A 100-word clear recommendation naming the restaurant
    "value_explanation": string,        // Explanation focused on overall experience, not just cost
    "restaurant_details": {
        "name": string,
        "price_range": string,
        "rating": float,
        "cuisine": string,
        "location": string,
        "features": [string]
    }
    }

    Be thoughtful and experience-oriented.
    Here are the restaurant options:
    {items_dict}
    """,
)
