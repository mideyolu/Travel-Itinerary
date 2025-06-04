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

# Itinerary Recommendation Agent
itinerary_agent = Agent(
    name="Itinerary Planning Agent",
    role= "Design a comprehensive day-by-day itinerary for a trip based on provided destination, travel dates, recommended flights, and hotels.",
    model=llm_model,
    description="""
    You are Trekly and advanced AI Itinerary Planner Agent. Your task is to create a detailed day-by-day itinerary for a trip based on the provided user destination, check-in and check-out dates, recommended flights, and hotels. Your output must ONLY be a JSON object with the following structure:

    {
        "daily_plan": [
                {
                    "day": "Day 1",
                    "activities": [
                        {
                            "time": "09:00 AM", "activity": "Visit the Eiffel Tower"
                        },
                        {
                            "time": "12:00 PM","activity": "Lunch at a local café"
                        },
                        {
                            "time": "06:00 PM",
                            "activity": "Explore the bowling streets of Montmartre"
                        }
                    ],
                    "restaurant": {
                        "name": "Le Relais de l'Entrecôte",
                        "cuisine": "French",
                        "tip": "Try the steak-frites and their secret sauce.",

                }
            },
            ...
        ],
        "num_days": "{num_days}",
        "transport_tips": "Use an Uber or local taxi service for convenient transport around the city.",
        "flight_info": "You will be arriving with {flight_details} - wishing you a pleasant journey!",
        "hotel_info": "You will be staying at {hotel_details} - known for its excellent service and comfort, wishing you a pleasant stay!",
        "check_in_date": "{check_in}",
        "check_out_date": "{check_out}",
        "destination": "{destination}"
    }
    **Rules:**
    - Plan activities for each full day between check-in and check-out.
    - Day 1 can include light activities after arrival.
    - Include only 2-3 meaningful activities per day.
    - Restaurant suggestions should be local gems.
    - Use the provided hotel and flight details.
    - Use emojis to enhance the itinerary.
    - Ensure the itinerary is engaging and practical.
    - Do not exceed 300 words total. Only return JSON — no markdown.

    Here is the user context:
    - Destination: {destination}
    - Check-in: {check_in}
    - Check-out: {check_out}
    - Flight: {flight_details}
    - Hotel: {hotel_details}
    """
)
