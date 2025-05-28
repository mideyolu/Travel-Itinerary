# logger.py

import logging
import logging.handlers
from app.core.config import settings

# Configure the logger
def get_logger(name:str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL.upper())

    # Create console handler
    handler = logging.StreamHandler()
    formatter= logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logging.addHandler(handler)


    return logger
