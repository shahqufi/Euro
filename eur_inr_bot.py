import os
import requests
from datetime import datetime, timedelta, timezone

# Read secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_random_meme():
    """Fetches a random meme from the free Meme API."""
    try:
        response = requests.get("https://meme-api.com/gimme", timeout=10)
        data = response.json()
        # Return a safe, family-friendly meme if possible
        if data.get("nsfw") or data.get("spoiler"):
            return get_random_meme() 
        return data.get("url"), data.get("title")
    except Exception as e:
        print(f"Error fetching meme: {e}")
        return None, None

def get_eur_inr_rate():
    url = "https://api.frankfurter.app/latest?from=EUR&to=INR"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        raw_date = data["date"]
        formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d %b %Y")
        return data["rates"]["INR"], formatted_date
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None, None

def send_telegram_message(rate, date, meme_url):
    if rate is None:
        print("No rate found.")
        return
        
    # Get the current time and convert to IST
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    time_ist = ist_now.strftime("%I:%M %p")
        
    # The detailed message layout
    message = (
        f"🚨💸 💶 <b>EURO TO RUPEE ALERT!</b> 💶 💸🚨\n"
        f"✨━━━━━━━━━━━━━━━━━━✨\n"
        f"🇪🇺 <b>1 EURO</b> ➡️ <b>{rate} INR</b> 🇮🇳🤑\n"
        f"✨━━━━━━━━━━━━━━━━━━✨\n"
        f"📅 Rate Date: {date} 📆\n"
        f"⏰ Checked at: <b>{time_ist} IST</b> 🇮🇳\n"
        f"🌐 Source: <a href='https://frankfurter.app'>Frankfurter API</a> 📊\n"
        f"🔥 Check your wallets! 💼💰🚀"
    )
    
    # 1. Send the Meme Photo first (if available)
    if meme_url:
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        photo_payload = {"chat_id": CHAT_ID, "photo": meme_url, "caption": "🎲 Random Meme of the Hour"}
        try:
            requests.post(photo_url, json=photo_payload, timeout=10)
        except Exception as e:
            print(f"Error sending meme: {e}")

    # 2. Send the Rate Message
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    
    try:
        response = requests.post(send_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"FAILED TO SEND. Telegram API responded with: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Fetch meme and rate, then send
    meme_url, meme_title = get_random_meme()
    rate, date = get_eur_inr_rate()
    send_telegram_message(rate, date, meme_url)
