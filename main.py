
import os
import time
import requests
from binance.client import Client
from twilio.rest import Client as TwilioClient

# Load environment variables
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_from = os.getenv("WHATSAPP_FROM")
whatsapp_to = os.getenv("WHATSAPP_TO")

# Binance client
client = Client(binance_api_key, binance_api_secret)

# Twilio client
twilio_client = TwilioClient(twilio_sid, twilio_auth_token)

def send_whatsapp_message(message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=f"whatsapp:{whatsapp_from}",
            to=f"whatsapp:{whatsapp_to}"
        )
        print("WhatsApp message sent:", message)
    except Exception as e:
        print("Failed to send WhatsApp message:", e)

def get_klines(symbol="BTCUSDT", interval="5m", limit=100):
    return client.get_klines(symbol=symbol, interval=interval, limit=limit)

def detect_breakout(candles):
    close_prices = [float(c[4]) for c in candles]
    resistance = max(close_prices[:-2])
    last_close = close_prices[-2]
    current_close = close_prices[-1]
    return last_close < resistance and current_close > resistance

def main():
    while True:
        try:
            candles = get_klines()
            if detect_breakout(candles):
                send_whatsapp_message("Breakout detected")
            time.sleep(60)
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
