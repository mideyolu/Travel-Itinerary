# main.py

from fastapi import FastAPI
from app.api.v1.endpoints import search_router
from app.core.config import settings
from app.core.logger import get_logger


# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="An AI-driven travel assistant",
    version="1.0.0"
)


# logger instance
logger = get_logger(__name__)
logger.info(f"Starting {settings.PROJECT_NAME} application...")


# Include the search router
app.include_router(
    search_router.router,
    tags=["Search"],
    prefix="/api/v1"
)

@app.get("/", tags=["Root"])
async def read_root():
    logger.info("Health check endpoint called")
    return {"message": "Welcome to the Treklyio API!"}
