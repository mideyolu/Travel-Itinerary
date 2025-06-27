# core/exceptions.py

from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(self, detail: str = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            status_code=status_code,
            detail=detail or "An unexpected error occurred"
        )

# General Custom Errors
class ServiceUnavailableError(BaseAppException):
    def __init__(self, detail: str = "Service is currently unavailable"):
        super().__init__(detail=detail)

class SerpApiServiceError(BaseAppException):
    def __init__(self, detail: str = "SerpApi service is unavailable"):
        super().__init__(detail=detail)

class SerpApiKeyError(BaseAppException):
    def __init__(self, detail: str = "SerpApi API key is not configured"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

class GeminiApiKeyError(BaseAppException):
    def __init__(self, detail: str = "Gemini API key is not configured"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

class AgentNotFoundError(BaseAppException):
    def __init__(self, detail: str = "Agent not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)

class AgentError(BaseAppException):
    def __init__(self, detail: str = "Agent processing failed"):
        super().__init__(detail=detail)

class MissingParameterError(BaseAppException):
    def __init__(self, detail: str = "Required parameter is missing"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

class EmptyResponseError(BaseAppException):
    def __init__(self, detail: str = "Missing response from agent"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

# Agent-Specific Errors
class FlightAgentError(BaseAppException):
    def __init__(self, detail: str = "Flight agent couldn't retrieve the data"):
        super().__init__(detail=detail, status_code=status.HTTP_502_BAD_GATEWAY)

class HotelAgentError(BaseAppException):
    def __init__(self, detail: str = "Hotel agent couldn't retrieve the data"):
        super().__init__(detail=detail, status_code=status.HTTP_502_BAD_GATEWAY)

class ItineraryPlannerAgentError(BaseAppException):
    def __init__(self, detail: str = "Itinerary planning failed"):
        super().__init__(detail=detail)
