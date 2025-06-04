# recommendation_service.py


from typing import List, Optional, Any
from app.agents.ai_agents import flight_agent, hotel_agent
from app.utils.custom_error import handle_custom_error
from app.core.logger import get_logger
from app.utils.function import extract_json_from_response

logger = get_logger(__name__)

# Function to get the appropriate agent based on the category
def get_agent(category: str):
    agents = {
        "flights": flight_agent,
        "hotels": hotel_agent,
    }
    agent = agents.get(category)
    if not agent:
        logger.error(f"No agent found for category: {category}")
    return agent

# Function to build the prompt for the agent
def build_prompt(category: str, items: List[Any]) -> str:
    return f"Given the provided {category} options, please recommend the best one:\n\n{items}"

# Function to generate a recommendation
async def generate_recommendation(category: str, items: List[Any]) -> Optional[dict]:
    try:
        logger.info(
            f"Generating recommendation for category: {category} with {len(items)} items."
        )

        if not items:
            logger.warning(f"No items provided for category: {category}")
            return f"No {category} available for recommendation."

        agent = get_agent(category)
        if not agent:
            return f"No AI recommendation available for {category} yet."

        prompt = build_prompt(category, items)
        response = agent.run(message=prompt)
        raw_output = str(response.content).strip()
        logger.debug(f"Raw response for {category}: {raw_output}")

        parsed_output = extract_json_from_response(raw_output)
        if parsed_output:
            logger.info(f"Parsed recommendation for {category} successful")
        return parsed_output

    except Exception as e:
        logger.error(f"Failed to generate recommendation for {category}: {str(e)}")
        handle_custom_error(e)
        return None
