import json
import re
import time
from app.utils.logging import logging
from app.core.exceptions import EmptyResponseError, MissingParameterError

def parse_and_validate_response(raw_result, validator_fn, agent_name):
    """
    Parses and validates the raw response from the agent.

    Args:
        raw_result (str): Raw response from the agent.
        validator_fn (callable): Function that validates the final parsed output.
        agent_name (str): Name to use in logs.

    Returns:
        dict: Validated agent response.

    Raises:
        Exception: If the response is invalid or cannot be parsed.
    """
    if not raw_result:
        raise EmptyResponseError("Empty response received from the agent.")

    cleaned = raw_result.strip()

    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    if not cleaned:
        raise EmptyResponseError("Empty response received after cleaning.")

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON: {str(e)}")

    if validator_fn(parsed):
        return parsed

    raise MissingParameterError(detail=f"Incomplete data for {agent_name}.")
