# agents/itinerary_agent.py

import json
from agno.agent import Agent
from app.utils.helpers import load_llm, load_serpapi_tools
from app.core.exceptions import ItineraryPlannerAgentError, MissingParameterError
from app.utils.logging import logging

# Itinerary Planner Agent
itinerary_agent = Agent(
    model=load_llm(),
    tools=[load_serpapi_tools().search_google],
    role="Plan detailed daily itineraries with activities, restaurants, and logistics for travel destinations.",
    show_tool_calls=True,
    markdown=False,
)


def generate_itinerary(prompt: str):
    """
     Use the itinerary agent to create a full travel plan for the destination.

    Returns:
       - json: A JSON object containing the recommended itineray plan based on the number of days to be spent.

    Raises:
        - MissingParameterError: If the prompt is not provided.
        - ItineraryPlannerAgentError: If there is an error in generating the itinerary.

    """
    # Validate the input
    if not prompt:
        logging.error(f"[ItineraryAgent] Missing Prompt  {prompt}")
        raise MissingParameterError(detail="Prompt is required to generate itinerary plans.")

    try:
        full_prompt = f"""
            You are Trekly and advanced AI Itinerary Planner Agent. Your task is to create a detailed day-by-day itinerary for a trip based on the provided user destination, check-in and check-out dates, recommended flights, and hotels.

            Return ONLY a JSON object in this format:

            {{
                 "daily_plan": [
                    {{
                        "day": "Day 1",
                        "activities": [
                            {{
                                "time": "09:00 AM", "activity": "Visit the Eiffel Tower"
                            }},
                            {{
                                "time": "12:00 PM", "activity": "Lunch at a local café"
                            }},
                            {{
                                "time": "06:00 PM", "activity": "Explore Montmartre"
                            }}
                        ],
                        "restaurant": {{
                            "name": "Le Relais de l'Entrecôte",
                            "cuisine": "French",
                            "tip": "Try the steak-frites and their secret sauce."
                        }}
                    }}
                ],
                "num_days": "7",
                "transport_tips": "Use Uber or local taxis for convenience.",
                "flight_info": "You will be arriving with {{flight_details}} - wishing you a pleasant journey!",
                "hotel_info": "You will be staying at {{hotel_details}} - enjoy your stay!",
                "check_in_date": "YYYY-MM-DD",
                "check_out_date": "YYYY-MM-DD",
                "destination": "Paris"
            }}

        {prompt}
        """

        result = itinerary_agent.run(
            message=full_prompt,
        )
        return json.loads(str(result.content).strip())

    except Exception as e:
        logging.error(f"[ItineraryAgent] Error: {str(e)}")
        raise ItineraryPlannerAgentError(detail=f"Error while generating itinerary: {str(e)}")
