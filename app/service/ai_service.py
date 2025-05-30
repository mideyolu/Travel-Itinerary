from typing import List
from app.models.schema import FlightInfo


async def generate_recommendation(category: str, items: List):
    if not items:
        return f"No {category} available for recommendation."

    if category == "flights":
        first = items[0]
        return (
            f"Try flying with {first.airline}, departing at {first.departure}, "
            f"arriving at {first.arrival}, costing around {first.price}."
        )

    return f"No AI recommendation available for {category} yet."
