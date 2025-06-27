# utils/logging.py
import logging
from typing import Optional


def configure_logger(
    name: str = "Trekly",
    level: int = logging.INFO,
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers: Optional[list] = None,
) -> logging.Logger:
    """
    Configure and return a customized logger instance.

    Args:
        name (str): Name to identify the logger (default: "Trekly")
        level (int): Logging level (default: logging.INFO)
        format (str): Log message format string
        handlers (Optional[list]): Additional logging handlers if needed

    Returns:
        logging.Logger: Configured logger instance

    """
    if handlers is None:
        handlers = [logging.StreamHandler()]

    logging.basicConfig(level=level, format=format, handlers=handlers)

    return logging.getLogger(name)


# Configure default logger instance
logger = configure_logger()
