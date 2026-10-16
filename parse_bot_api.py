import requests

from config import API_URL, PARSE_API_KEYS, SEARCH_FILTERS
from db import get_meta, set_meta
from notifier import notify_configured

# Statuses meaning "this key is expired / out of credit / invalid".
KEY_FAILURE_STATUSES = {401, 402, 403}


def _label(key):
    return f"...{key[-4:]}"


def _active_index(conn):
    """Resume from the key that last worked, so we don't retry dead keys every run."""
    saved = get_meta(conn, "active_key_suffix")
    for i, key in enumerate(PARSE_API_KEYS):
        if saved and key.endswith(saved):
            return i
    return 0


def _fetch_all(key):
    headers = {"X-API-Key": key}
    params = dict(SEARCH_FILTERS)
    vehicles = []
    page = 1
    while True:
        params["page"] = page
        resp = requests.get(API_URL, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()["data"]
        vehicles.extend(data["vehicles"])
        if len(vehicles) >= data["total"] or not data["vehicles"]:
            return vehicles
        page += 1


def fetch_vehicles(conn):
    start = _active_index(conn)
    for i in range(start, len(PARSE_API_KEYS)):
        key = PARSE_API_KEYS[i]
        try:
            vehicles = _fetch_all(key)
        except requests.HTTPError as e:
            if e.response is None or e.response.status_code not in KEY_FAILURE_STATUSES:
                raise
            if i + 1 < len(PARSE_API_KEYS):
                notify_configured(
                    f"⚠️ car-finder: Parse API key {_label(key)} failed "
                    f"(HTTP {e.response.status_code}, likely expired). "
                    f"Rotating to key {_label(PARSE_API_KEYS[i + 1])}."
                )
                continue
            notify_configured(
                f"🛑 car-finder: all {len(PARSE_API_KEYS)} Parse API keys have failed. "
                "Add a new key to PARSE_API_KEYS."
            )
            raise
        set_meta(conn, "active_key_suffix", key[-6:])
        return vehicles
