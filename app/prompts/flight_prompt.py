# prompts/flight_prompt.py

from app.models.schemas import FlightSearchRequest

def build_flight_prompt(request: FlightSearchRequest) -> str:
    """
    Build a prompt for the flight recommendation agent based on structured user input.

    Args:
        request (FlightSearchRequest): Object containing flight search input such as:
                    (departure_id, arrival_id, outbound_date, return_date, and currency)

    Returns:
        str: A formatted prompt string that instructs the LLM agent to use SerpAPI's
             Google Flights engine
    """

    prompt = (
        f"Search for flights from {request.departure_id} to {request.arrival_id} "
        f"on {request.outbound_date}."
    )

    if request.return_date:
        prompt += f" Return on {request.return_date}."

    prompt += f" Show prices in {request.currency or 'USD'}."

    prompt += f"""
        You are a part of Trekly a travel assistant using the `google_flights` engine, which is connected to the SerpAPI.

        Your job is to:
        1. Perform a real-time flight search based on the user's request.
        2. You **must** use the SerpAPI Google Flights engine. The returned JSON contains either `best_flights` or `other_flights` fields.
        3. Extract all required flight information **from the SerpAPI response** fields — do **not guess** or make up any value.

        From the flight response, extract:
        - `airline`: from `airline` inside each flight object
        - `airline_logo`: from `airline_logo`
        - `departure`: name of the first `departure_airport.name`
        - `arrival`: name of the last `arrival_airport.name`
        - `departure_time`: from the first `departure_airport.time`
        - `arrival_time`: from the last `arrival_airport.time`
        - `duration`: sum or description of total duration across all segments
        - `travel_class`: from `travel_class`
        - `price`: if available, from the aggregated pricing (add currency symbol)

        4. **DO NOT** fabricate any data. If any critical field is missing, discard that flight or log as null.

        5. Select the **most balanced option** using the `best_flights` list if available, falling back to `other_flights`.

        6. If `airline_logo` is missing, perform a secondary `search_google` using this format:
        "{{airline name}} logo PNG" and extract a logo URL if possible.

        Respond strictly in this format:
        {{
            "flight_details": {{
                "airline": string,
                "airline_logo": string or null,
                "travel_class": string,
                "price": string,         // include currency symbol
                "duration": string,      // include minutes or hrs symbol at the end
                "departure": string,
                "arrival": string,
                "departure_time": string,
                "arrival_time": string
            }},
            "recommendation": string,
            "value_explanation": string,
            "source_link": string
        }}

        Recommendation Criteria:
        - Comfort (travel class, amenities, layovers) : Consider factors like travel class, and duration that impact the passenger's experience.
        - Convenience: Evaluate timing (departure/arrival), and total duration in terms of travel ease.
        - Price vs value : if it contributes meaningfully to the overall recommendation—don't prioritize it above comfort and convenience.
        - Travel Class: Explain why the comfort and benefits of the travel class stand out.
        - Airline reliability

        User Request:
        {prompt}
    """

    return prompt.strip()
