from pydantic import BaseModel
from typing import List

# Itinerary plan generic schemas
# Restaurant
class Restaurant(BaseModel):
    """Model for restaurant details."""
    name: str
    cuisine: str
    tip: str

# Activity
class Activity(BaseModel):
    """Model for activity details."""
    time: str
    activity: str

# Day Plan
class DayPlan(BaseModel):
    """Model for daily itinerary plan."""
    day: str
    activities: List[Activity]
    restaurant: Restaurant
