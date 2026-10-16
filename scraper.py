from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from db import filter_new_lots, init_db, mark_seen
from notifier import notify_new_vehicles
from parse_bot_api import fetch_vehicles


def main():
    conn = init_db()
    vehicles = fetch_vehicles()
    new_vehicles = filter_new_lots(conn, vehicles)

    print(f"Fetched {len(vehicles)} vehicles, {len(new_vehicles)} new.")

    if new_vehicles:
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            notify_new_vehicles(new_vehicles)
        else:
            print("Telegram not configured yet, skipping notification.")

    mark_seen(conn, vehicles)
    conn.close()


if __name__ == "__main__":
    main()
