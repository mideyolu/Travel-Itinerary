# ai_service.py

import json
import re
from typing import List
from app.agents.ai_agents import flight_agent, hotel_agent

from app.core.logger import get_logger


logger = get_logger(__name__)


async def generate_recommendation(category: str, items: List):

    logger.info(f"Generating recommendation for category: {category} with {len(items)} items.")

    if not items:
        logger.error(f"No items provided for category: {category}")
        return f"No {category} available for recommendation."

    agent = {
        "flights": flight_agent,
        "hotels": hotel_agent,

    }.get(category)

    if not agent:
        logger.error(f"No agent found for category: {category}")
        return f"No AI recommendation available for {category} yet."

    prompt = f"Given the provided {category} options, please recommend the best one:\n\n{items}"

    response = agent.run(message=prompt)
    raw_output = str(response.content)

    print(raw_output)

    # Remove triple backticks and extract JSON safely
    try:
        json_str = re.search(r"\{.*\}", raw_output, re.DOTALL).group()
        parsed_output = json.loads(json_str)
        print(parsed_output)
        return parsed_output
    except Exception as e:
        logger.error(f"Failed to parse JSON for {category}: {e}")
        return f"Failed to parse AI response for {category}."
