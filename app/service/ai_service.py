# ai_service.py

from typing import List


async def generate_recommendation(category: str, items: List):
    if not items:
        return f"No {category} available for recommendation."

    first = items[0]

    if category == "flights":
        return (
            f"Try flying with {first.airline},\n"
            f"departing at {first.departure}, "
            f"arriving at {first.arrival}"
            f"Costing around {first.price}."
            f" Duration is {first.duration}."
        )

    elif category == "hotels":
        return (
            f"Consider staying at {first.name}, rated {first.rating} stars, "
            f"Starting from {first.price_per_night}."
        )

    elif category == "restaurants":
        return (
            f"You might enjoy dining at {first.title}, located at {first.address}, "
            f"known for a {first.rating} stars."
        )

    return f"No AI recommendation available for {category} yet."
