# utils/api_loader.py

from serpapi.google_search import GoogleSearch
from app.core.exceptions import SerpApiServiceError
from app.utils.logging import logging
from typing import Optional

class SerpApiTools:
    """
        A wrapper class for SerpAPI services providing flight, hotel, and general search capabilities.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_flights(
        self,
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
        return_date: Optional[str] = None,
        currency: str = "USD",
    ):
        """
        Search for flights using SerpAPI's Google Flights engine.

        Args:
            departure_id (str): IATA code for departure airport
            arrival_id (str): IATA code for arrival airport
            outbound_date (str): Departure date in YYYY-MM-DD format
            return_date (Optional[str]): Return date in YYYY-MM-DD format (optional for one-way trips)
            currency (str): Currency code for pricing

        Returns:
            dict: Flight search results in SerpAPI's response format

        Raises:
            SerpApiServiceError: If the search fails or API returns an error
        """
        try:
            params = {
                "engine": "google_flights",
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "outbound_date": outbound_date,
                "currency": currency,
                "api_key": self.api_key,
            }
            if return_date:
                params["return_date"] = return_date

            search = GoogleSearch(params)
            return search.get_dict()
        except Exception as e:
            logging.error(f"[SerpApiTools] Google Flights search failed: {e}")
            raise SerpApiServiceError()

    def search_hotels(
        self,
        arrival_id: str,
        check_in_date: str,
        check_out_date: str,
        currency: str = "USD",
    ):
        """
        Search for hotels using SerpAPI's Google Hotels engine.

        Args:
            arrival_id (str): IATA code (e.g. "CDG")
            check_in_date (str): Check-in date in YYYY-MM-DD format
            check_out_date (str): Check-out date in YYYY-MM-DD format
            currency (str): Currency code for pricing

        Returns:
            dict: Hotel search results in SerpAPI's response format

        Raises:
            SerpApiServiceError: If the search fails or API returns an error
        """
        try:
            params = {
                "engine": "google_hotels",
                "q": arrival_id,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "currency": currency,
                "api_key": self.api_key,
            }

            search = GoogleSearch(params)
            return search.get_dict()
        except Exception as e:
            logging.error(f"[SerpApiTools] Google Hotels search failed: {e}")
            raise SerpApiServiceError()


    def search_google(self, query: str):
        """
        Perform a general Google search through SerpAPI.

        Args:
            query (str): The search query string

        Returns:
            dict: Google search results in SerpAPI's response format

        Raises:
            SerpApiServiceError: If the search fails or API returns an error

        """
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
            }

            search = GoogleSearch(params)
            return search.get_dict()
        except Exception as e:
            logging.error(f"[SerpApiTools] General Google Search failed: {e}")
            raise SerpApiServiceError()
