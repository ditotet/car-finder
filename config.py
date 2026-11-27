import os

from dotenv import load_dotenv

load_dotenv()

# Comma-separated list, tried in order; rotates to the next when one expires.
# Falls back to the single PARSE_API_KEY for backwards compatibility.
PARSE_API_KEYS = [
    k.strip()
    for k in (os.environ.get("PARSE_API_KEYS") or os.environ["PARSE_API_KEY"]).split(",")
    if k.strip()
]
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

SCRAPER_ID = "2adeb1e1-947a-4c71-88b5-5ef2feb90fad"
API_URL = f"https://api.parse.bot/scraper/{SCRAPER_ID}/search_vehicles"

SEARCH_FILTERS = {
    "make": "Tesla",
    "model": "Model 3",
    "year_from": 2026,
    "year_to": 2026,
}

# Only keep dual-motor (AWD) cars: Premium AWD or Performance.
# Tesla VIN position 8 is the motor code: A = single motor RWD,
# B = dual motor AWD, T = dual motor Performance.
AWD_VIN_MOTOR_CODES = {"B", "T"}
RWD_VIN_MOTOR_CODES = {"A"}
AWD_DRIVE_TYPE = 2

DB_PATH = os.environ.get("DB_PATH", "seen.db")
