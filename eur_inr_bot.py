import os
import requests

# Read secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_eur_inr_rate():
    url = "https://api.frankfurter.app/latest?from=EUR&to=INR"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["rates"]["INR"], data["date"]
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None, None

def send_telegram_message(rate, date):
    if rate is None:
        print("No rate found.")
        return
        
    print(f"Attempting to send to Chat ID: {CHAT_ID}")
    print(f"Using Token: {TELEGRAM_TOKEN[:5]}...{TELEGRAM_TOKEN[-5:] if TELEGRAM_TOKEN else ''}") # Prints partial token for security
    
    message = f"💶➡️🇮🇳 **EUR to INR Rate**\n\n1 EUR = {rate} INR\n📅 Rate Date: {date}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(send_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"FAILED TO SEND. Telegram API responded with: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    rate, date = get_eur_inr_rate()
    send_telegram_message(rate, date)
