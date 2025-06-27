# agents/agents.py

from app.agents.agents_factory import create_agent
from app.utils.helpers import load_serpapi_tools

# Flight Agent
flight_agent = create_agent(
    role="Handle flight search and recommendation based on received data.",
    tools=[load_serpapi_tools().search_flights],
)

# Hotel Agent
hotel_agent = create_agent(
    role="Handle hotel search and recommendation based on received data.",
    tools=[
        load_serpapi_tools().search_google,
        load_serpapi_tools().search_hotels,
    ],
)

# Itinerary Agent
itinerary_agent = create_agent(
    role="Plan detailed daily itineraries with activities, restaurants, and logistics for travel destinations.",
    tools=[load_serpapi_tools().search_google],
)
