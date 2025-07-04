# Import custom modules
from flight_data import FlightData
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import time

# STEP 1: Initialize classes to manage data, flight search, and notifications
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notifier = NotificationManager()

# STEP 2: Check if any destination in the sheet is missing an IATA code
# If missing, fetch the IATA code using city name and update the sheet
if any(row["iataCode"] == "" for row in sheet_data):
    for row in sheet_data:
        # Fetch IATA code for the city
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(1.5)  # Avoid hitting API rate limits
    # Save updated data back to the sheet
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# STEP 3: Search for flights between two cities (example: Delhi to Mumbai)
flight = flight_search.check_flight("DEL", "BOM")

# STEP 4: If a flight deal is found, send a WhatsApp notification
if flight:
    message = (
        f"✈️ Low Price Alert!\n"
        f"Only ₹{flight.price} to fly from {flight.origin_airport} to {flight.destination_airport}.\n"
        f"Departure: {flight.out_date} | Return: {flight.return_date}\n"
        f"Book now!"
    )
    notifier.send_whatsapp(message)
else:
    print("❌ No flight found — skipping notification.")
