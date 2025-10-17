#!/usr/bin/env python3
"""
weather_extract.py
Fetch current weather data for London using WeatherAPI.
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.getenv("WEATHER_API_KEY", "bfa54e11161748918ff230153251610")
BASE_URL = "https://api.weatherapi.com/v1/current.json"
CITY = "London"

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "weather" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_weather():
    params = {"key": API_KEY, "q": CITY, "aqi": "no"}
    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def normalize_weather(raw):
    c = raw["current"]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": raw["location"]["name"],
        "country": raw["location"]["country"],
        "temp_c": c["temp_c"],
        "condition": c["condition"]["text"],
        "wind_kph": c["wind_kph"],
        "humidity": c["humidity"],
        "cloud": c["cloud"],
        "pressure_mb": c["pressure_mb"],
        "feelslike_c": c["feelslike_c"],
        "precip_mm": c["precip_mm"],
        "uv": c["uv"],
    }


def main():
    print("[*] Fetching weather data for London…")
    raw = fetch_weather()
    weather = normalize_weather(raw)

    out_file = OUT_DIR / f"weather_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w") as f:
        json.dump(weather, f, indent=2)

    print(f"[+] Saved weather data → {out_file}")
    print(json.dumps(weather, indent=2))


if __name__ == "__main__":
    main()
