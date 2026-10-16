import requests

from config import API_URL, PARSE_API_KEY, SEARCH_FILTERS


def fetch_vehicles():
    headers = {"X-API-Key": PARSE_API_KEY}
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
            break
        page += 1
    return vehicles
