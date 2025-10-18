#!/usr/bin/env python3
"""
weather_extract.py
Fetches weather for coordinates (lat, lon).
Usage:
  python3 weather_extract.py --lat 52.4862 --lon -1.8904
"""

import argparse
import json
import os
import logging
from datetime import datetime, UTC
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    return p.parse_args()

def main():
    args = parse_args()
    lat, lon = args.lat, args.lon

    API_KEY = os.getenv("WEATHER_API_KEY", "bfa54e11161748918ff230153251610")
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": f"{lat},{lon}", "aqi": "no"}

    out_dir = Path(__file__).resolve().parents[2] / "data" / "weather" / "processed"
    raw_dir = Path(__file__).resolve().parents[2] / "data" / "weather" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Fetching weather for {lat},{lon}")
    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    city = raw.get("location", {}).get("name", "Unknown")
    region = raw.get("location", {}).get("region", "")
    country = raw.get("location", {}).get("country", "")

    # normalize
    c = raw.get("current", {})
    
    if c.get("temp_c") is None:
        logger.warning("Weather API returned incomplete data; skipping write.")
        return 1

    normalized = {
        "timestamp": datetime.now(UTC).isoformat(),
        "city": city,
        "region": region,
        "country": country,
        "lat": raw.get("location", {}).get("lat"),
        "lon": raw.get("location", {}).get("lon"),
        "temp_c": c.get("temp_c"),
        "condition": c.get("condition", {}).get("text"),
        "wind_kph": c.get("wind_kph"),
        "humidity": c.get("humidity"),
        "cloud": c.get("cloud"),
        "pressure_mb": c.get("pressure_mb"),
        "feelslike_c": c.get("feelslike_c"),
        "precip_mm": c.get("precip_mm"),
        "uv": c.get("uv"),
    }

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    raw_path = raw_dir / f"weather_raw_{city.replace(' ', '_')}_{timestamp}.json"
    processed_path = out_dir / f"weather_{city.replace(' ', '_')}_{timestamp}.json"

    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2)
    with open(processed_path, "w") as f:
        json.dump(normalized, f, indent=2)

    logger.info(f"Saved weather processed file: {processed_path}")
    print(processed_path)
    return 0

if __name__ == "__main__":
    exit(main())
