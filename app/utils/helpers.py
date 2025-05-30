# helper.py
from functools import lru_cache
from datetime import datetime


# Helper function to parse date strings in the format YYYY-MM-DD
@lru_cache()
def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_str}. Expected format is YYYY-MM-DD.") from e
