# search_services.py
from app.utils.function import make_serpapi_request

class SerpAPIService:

    # Flgith Search Function
    @staticmethod
    async def search_flights(query: dict):
        """
        Search for flights using the SerpAPI service.
        """

        return await make_serpapi_request(
            engine="google_flights", query=query, error_context="Flight Search"
        )

    # Hotel Search Function
    @staticmethod
    async def search_hotels(query: dict):
        """
        Search for hotels using the SerpAPI service.
        """

        return await make_serpapi_request(
            engine="google_hotels", query=query, error_context="Hotel Search"
        )

