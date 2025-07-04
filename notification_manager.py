from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials and phone numbers from environment
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM")  # Example: 'whatsapp:+14155238886'
TWILIO_TO = os.environ.get("TWILIO_TO")      # Your verified WhatsApp number

class NotificationManager:
    """
    This class is responsible for sending notifications via WhatsApp using Twilio API.
    """

    def send_whatsapp(self, message):
        """
        Sends a WhatsApp message to the user with the given text.
        """
        # Initialize Twilio client with SID and Auth Token
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        # Send message using Twilio's WhatsApp API
        message = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )

        # Confirm message was sent successfully
        print(f"✅ WhatsApp message sent. SID: {message.sid}")
