# agents/agent_factory.py

from agno.agent import Agent
from app.utils.helpers import load_llm, load_serpapi_tools

def create_agent(role: str, tools: list):
    return Agent(
        model=load_llm(),
        tools=tools,
        role=role,
        show_tool_calls=True,
        markdown=False,
        use_json_mode=True
    )
