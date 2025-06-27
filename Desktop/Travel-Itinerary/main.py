# main.py

from fastapi import FastAPI
from app.api.v1.routers import router as api_router

app = FastAPI(
    title="Trekly Travel Planner API",
    description="API for generating travel itineraries using multi-agent workflows.",
    version="1.0.0",
)

app.include_router(api_router)
