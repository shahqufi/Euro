import os
import requests

# Read secrets from GitHub Actions environment variables
TELEGRAM_TOKEN = os.environ.get("8915784825:AAEYCYTD2US8YIEZ8f_dZZDDBpAkmkaIGIQ")
CHAT_ID = os.environ.get("CHAT_ID")

def get_eur_inr_rate():
    """Fetches the latest EUR to INR exchange rate."""
    url = "https://api.frankfurter.app/latest?from=EUR&to=INR"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"]["INR"], data["date"]
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None, None

def send_telegram_message(rate, date):
    """Sends the rate to your Telegram chat."""
    if rate is None:
        return
    message = f"💶➡️🇮🇳 **EUR to INR Rate**\n\n1 EUR = {rate} INR\n📅 Rate Date: {date}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        requests.post(send_url, json=payload, timeout=10)
        print("Message sent successfully.")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    rate, date = get_eur_inr_rate()
    send_telegram_message(rate, date)
