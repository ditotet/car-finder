import os

from dotenv import load_dotenv

load_dotenv()

PARSE_API_KEY = os.environ["PARSE_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

SCRAPER_ID = "2adeb1e1-947a-4c71-88b5-5ef2feb90fad"
API_URL = f"https://api.parse.bot/scraper/{SCRAPER_ID}/search_vehicles"

SEARCH_FILTERS = {
    "make": "Tesla",
    "model": "Model S",
    "year_from": 2021,
    "year_to": 2024,
}

DB_PATH = os.environ.get("DB_PATH", "seen.db")
