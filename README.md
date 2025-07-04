# ✈️ Flight Price Tracker

A Python automation project that checks and notifies you of the **lowest flight prices** between cities using real-time data from the **Amadeus Flight Offers API**, with data storage in **Google Sheets**, and **WhatsApp alerts via Twilio**.

---

## 🚀 Tech Stack

- **Python 3**
- **Amadeus API** (for flight offers and IATA codes)
- **Sheety API** (for Google Sheets as database)
- **Twilio API** (for WhatsApp notifications)
- `requests`, `datetime`, `dotenv`, `pprint`

---

## 📌 Features

- 🔎 Fetches IATA codes from city names using Amadeus API  
- 📋 Stores destination and price threshold in Google Sheets  
- 💰 Monitors flight prices daily  
- 📲 Sends WhatsApp alerts when a good deal is found  
- 🧱 Modular, class-based code (`FlightData`, `DataManager`, etc.)  
- 🔐 Secrets managed using `.env` file (excluded from repo)  

---

## 🗂️ Project Structure

flight-price-tracker/
├── data_manager.py
├── flight_data.py
├── flight_search.py
├── notification_manager.py
├── main.py
├── .env.example
└── README.md


---

## 📁 How to Run

1. Clone this repo  
2. Create a `.env` file using `.env.example` as template  
3. Fill in your credentials  
4. Run `main.py`

---

## 🙌 Contributions

Feel free to fork and enhance this project. PRs are welcome!

---

## 🪪 License

MIT License.
