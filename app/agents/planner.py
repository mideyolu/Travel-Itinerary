# agents/planner.py

from app.utils.logging import logging


def fill_missing_fields(target, source, prefer_dates_from=None):
    """
    Auto-fills missing fields in `target` using values from `source`.

    Args:
        target (Any): The model to be filled.
        source (Any): The model providing fallback values.
        prefer_dates_from (Any, optional): If provided, use this source for check_in/check_out.
    """

    # Destination
    if not target.destination and hasattr(source, "destination"):
        target.destination = source.destination
        logging.debug(f"Auto-filled `destination` from {source.__class__.__name__}")

    if not target.destination and hasattr(source, "arrival_id"):
        target.destination = source.arrival_id
        logging.debug(f"Auto-filled `destination` from {source.__class__.__name__}")

    # Dates - always prefer `prefer_dates_from` if given
    date_source = prefer_dates_from or source

    if not target.check_in_date and hasattr(date_source, "outbound_date"):
        target.check_in_date = date_source.outbound_date
        logging.debug(
            f"Auto-filled `check_in_date` from {date_source.__class__.__name__}"
        )

    if not target.check_out_date and hasattr(date_source, "return_date"):
        target.check_out_date = date_source.return_date
        logging.debug(
            f"Auto-filled `check_out_date` from {date_source.__class__.__name__}"
        )

    # Currency
    if hasattr(target, "currency") and not target.currency:
        target.currency = getattr(source, "currency", "USD") or "USD"
        logging.debug(f"Auto-filled `currency` from {source.__class__.__name__}")


async def execute_agent(name: str, func, request, exception_class):
    """
    Executes an agent function with logging and custom error handling.

    Args:
        name (str): Agent name.
        func (Callable): The async function to call.
        request: Request payload.
        exception_class: Exception to raise on error.

    Returns:
        Result from agent.
    """
    try:
        logging.info(f"{name} Agent Starting...")
        result = await func(request)
        logging.info(f"{name} Agent Complete")
        return result
    except Exception as e:
        logging.error(f"{name} Agent Failed: {str(e)}")
        raise exception_class(detail=f"{name} Agent Error: {str(e)}")
