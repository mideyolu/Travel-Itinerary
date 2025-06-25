# agents/hotel_agent.py

from agno.agent import Agent
from app.utils.helpers import load_llm, load_serpapi_tools

# Initializing the flight agent
hotel_agent = Agent(
    model=load_llm(),
    tools=[load_serpapi_tools().search_hotels,
           load_serpapi_tools().search_google],
    role="Handle hotel search and recommendation based on received data.",
    show_tool_calls=True,
    markdown=False,
    use_json_mode=True
)
