# agents/itinerary_agent.py

import json
from agno.agent import Agent
from app.utils.helpers import load_llm, load_serpapi_tools


# Itinerary Planner Agent
itinerary_agent = Agent(
    model=load_llm(),
    tools=[load_serpapi_tools().search_google],
    role="Plan detailed daily itineraries with activities, restaurants, and logistics for travel destinations.",
    show_tool_calls=True,
    markdown=False,
)
