import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pprint import pprint

# Load environment variables from the .env file
load_dotenv()

# API endpoint for Sheety to interact with your Google Sheet
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/c8487cc7acc6613f2f880a7e58bd0ee7/flightDeals/destinations"

class DataManager:
    """
    This class is responsible for:
    - Retrieving flight destination data from Google Sheets via Sheety API
    - Updating the sheet with missing IATA codes
    """

    def __init__(self):
        # Load Sheety username and password from environment variables
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]

        # Basic authentication for Sheety API
        self._authorization = HTTPBasicAuth(self._user, self._password)

        # This will store the sheet data
        self.destination_data = {}

    def get_destination_data(self):
        """
        Fetch destination data from Google Sheet using Sheety API.
        Returns the sheet data in JSON format.
        """
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        print("📡 Response status code:", response.status_code)
        print("📨 Response body:", response.text)
        data = response.json()

        # Pretty print the sheet data (useful for debugging)
        print("📋 Destination Data:")
        for destination in data["destinations"]:
            print(f"📍 {destination['city']} ({destination['iataCode']}) - ₹{destination['lowestPrice']}")

        # Store and return the list of destinations
        self.destination_data = data["destinations"]
        return self.destination_data

    def update_destination_codes(self):
        """
        Update the IATA codes in the Google Sheet using PUT requests.
        Iterates through each row and updates the corresponding entry.
        """
        for city in self.destination_data:
            new_data = {
                "destinations": {
                    "iataCode": city["iataCode"]
                }
            }

            # Send the updated data to the Sheety API using the row ID
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )

            # Print the API response (for confirmation/debugging)
            print(response.text)
