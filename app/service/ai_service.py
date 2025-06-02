# ai_service.py
from typing import List
from app.agents.ai_agents import flight_agent, hotel_agent, restaurant_agent
from agno.utils.pprint import pprint_run_response


async def generate_recommendation(category: str, items: List):
    if not items:
        return f"No {category} available for recommendation."

    items_dict = [
        items.__dict__ if hasattr(items, "__dict__") else items for items in items
    ]

    prompt = f"Given the provided {category} options, please recommend the best one:\n\n{items_dict}"

    agent = {
        "flights": flight_agent,
        "hotels": hotel_agent,
        "restaurants": restaurant_agent,
    }.get(category)

    if not agent:
        return f"No AI recommendation available for {category} yet."

    response = agent.run(message=prompt)

    formatted_response = pprint_run_response(response, markdown=False, show_time=True)

    print(f"Generated {category} recommendation:", formatted_response)

    return formatted_response
