# core/exceptions.py

from fastapi import HTTPException , status

# General Custom errros for the application

class SerpApiServiceError(HTTPException):
    def __init__(self, detail: str = "SerpApi api service is unavailable"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class SerpApiKeyError(HTTPException):
    def __init__(self, detail: str = "Api key is not configured"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class GeminiApiKeyError(HTTPException):
    def __init__(self, detail: str = "Gemini api key is not configured"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class AgentNotFoundError(HTTPException):
    def __init__(self, detail: str = "Agent not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class AgentError(HTTPException):
    def __init__(self, detail: str = "Agent processing failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )

class MissingParameterError(HTTPException):
    def __init__(self, detail: str = "Required parameter is missing"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

# Agent specific errors
class FlightAgentError(HTTPException):
    def __init__(self, detail: str= "Flight agent couldn't retrieve the data"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )

class HotelAgentError(HTTPException):
    def __init__(self, detail: str= "Hotel agent couldn't retrieve the data"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )

class ItineraryPlannerAgentError(HTTPException):
    def __init__(self, detail: str= "Itinerary planning failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
