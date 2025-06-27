# utils/request.py

import json
import re
import time
from app.utils.logging import logging
from app.utils.parser import parse_and_validate_response

async def run_agent_with_retries(agent, prompt: str, validator_fn, agent_name: str, max_retries: int = 3, retry_delay: int = 2):
    """
    Generic runner for invoking LLM agents with retries and response validation for flight and hotel recommendation.

    Args:
        agent: Instantiated agent object (e.g., flight_agent or hotel_agent).
        prompt (str): Prompt message passed to the agent.
        validator_fn (callable): Function that validates the final parsed output.
        agent_name (str): Name to use in logs.
        max_retries (int): Number of retry attempts.
        retry_delay (int): Delay between retries in seconds.

    Returns:
        dict: Validated agent response.

    Raises:
        Exception: If the agent fails after retries or doesn't return valid data.
    """

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"[{agent_name}] Attempt {attempt} running agent...")
            result = agent.run(message=prompt)

            if not result.tools:
                raise Exception("SerpApi tool was not used. Agent must call the tool.")

            raw_result = result.content
            logging.info(f"[{agent_name}] Raw Result: \n{raw_result}")
            logging.debug(f"[{agent_name}] Used tools: {result.tools}")

            parsed_response = parse_and_validate_response(raw_result, validator_fn, agent_name)

            return parsed_response

        except Exception as e:
            logging.error(f"[{agent_name}] Error on attempt {attempt}: {str(e)}")
            time.sleep(retry_delay)

    raise Exception(
        f"[{agent_name}] Failed to get valid recommendation after {max_retries} attempts."
    )
