import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def format_message(vehicle):
    return (
        f"🚗 {vehicle['name']}\n"
        f"Lot: {vehicle['lot']}\n"
        f"VIN: {vehicle['vin']}\n"
        f"Location: {vehicle['location']}\n"
        f"Damage: {vehicle['primary_damage']}\n"
        f"Current bid: {vehicle['current_bid']}\n"
        f"Est. value: ${vehicle['estimated_min']}-${vehicle['estimated_max']}\n"
        f"Time left: {vehicle['time_left']}\n"
        f"https://bid.cars/en/lot/{vehicle['lot']}"
    )


def send_telegram_message(text, photo_url=None):
    if photo_url:
        resp = requests.post(
            f"{TELEGRAM_API}/sendPhoto",
            data={"chat_id": TELEGRAM_CHAT_ID, "caption": text[:1024]},
            params={"photo": photo_url},
            timeout=30,
        )
    else:
        resp = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=30,
        )
    resp.raise_for_status()


def notify_configured(text):
    """Send a plain Telegram message if Telegram is set up; otherwise just print it."""
    print(text)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram_message(text)


def notify_new_vehicles(vehicles):
    for vehicle in vehicles:
        text = format_message(vehicle)
        photo_url = vehicle["photos"][0] if vehicle.get("photos") else None
        send_telegram_message(text, photo_url)
