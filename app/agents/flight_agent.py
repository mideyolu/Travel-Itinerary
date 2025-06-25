# agent/flight_agent.py

from agno.agent import Agent
from app.utils.helpers import load_llm, load_serpapi_tools

# Initializing the flight agent
flight_agent = Agent(
        model=load_llm(),
        tools=[load_serpapi_tools().search_flights],
        role="Handle flight search and recommendation based on received data.",
        show_tool_calls=True,
        markdown=False,
        use_json_mode=True,
)
