from flight_data import FlightData
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Endpoint to get access token from Amadeus API
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    """
    This class is responsible for:
    - Getting IATA codes for cities using Amadeus API
    - Searching for flights using city IATA codes
    """

    def __init__(self):
        # Fetch Amadeus API credentials from environment variables
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]

        # Get a new bearer token for authorization
        self._token = self._get_new_token()

    def _get_new_token(self):
        """
        Get a fresh bearer token from Amadeus API to authenticate future requests.
        """
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        token_data = response.json()

        # Print token info for debugging
        print(f"🪪 Your token is: {token_data['access_token']}")
        print(f"⏳ Token expires in: {token_data['expires_in']} seconds")

        return token_data['access_token']

    def get_destination_code(self, city_name):
        """
        Given a city name, return the IATA airport code using Amadeus API.
        Fallback for known cities like Tokyo is built-in.
        """
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }

        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data["data"]:
            # Optional fallback: Hardcoded for known edge cases like Tokyo
            if city_name.lower() == "tokyo":
                print("✅ Fallback triggered: Tokyo → TYO")
                return "TYO"
            print(f"⚠️ No IATA code found for {city_name}")
            return None

        code = data["data"][0]["iataCode"]
        print(f"✅ {city_name} → IATA Code: {code}")
        return code

    def check_flight(self, origin_city_code, destination_city_code):
        """
        Search for available flight offers between two IATA codes.
        Returns key flight info: price, airports, and travel dates.
        """
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        # Define date range for flight search: from tomorrow to 6 months later
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        six_months_later = today + timedelta(days=180)

        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": tomorrow.strftime("%Y-%m-%d"),
            # Optional: "returnDate": six_months_later.strftime("%Y-%m-%d")
            "adults": 1,
            # Optional: "nonStop": True
            "max": 5,
            "currencyCode": "INR"
        }

        # Make the flight search request
        response = requests.get(url=url, headers=headers, params=params)

        try:
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Error while fetching flights: {e}")
            return None

        data = response.json()

        if not data.get("data"):
            print(f"🔍 No flights found from {origin_city_code} to {destination_city_code}")
            return None

        # Extract first matching flight offer
        flight_data = data["data"][0]
        itinerary = flight_data["itineraries"][0]["segments"]

        return FlightData(
            price=flight_data["price"]["total"],
            origin_airport=itinerary[0]["departure"]["iataCode"],
            destination_airport=itinerary[-1]["arrival"]["iataCode"],
            out_date=itinerary[0]["departure"]["at"].split("T")[0],
            return_date="N/A"
        )

