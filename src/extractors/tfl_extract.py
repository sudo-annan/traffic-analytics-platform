#!/usr/bin/env python3
"""
tfl_extract.py
Fetch current London road disruptions and road status from TfL Unified API.

Workflow:
1️⃣ Fetch live data from TfL endpoints.
2️⃣ Save full raw JSONs into data/tfl/raw/.
3️⃣ Normalize and merge both into one combined JSON.
4️⃣ Save processed combined JSON into data/tfl/processed/ (used by ETL).

Author: Annan (Full Stack Developer Assessment)
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path


# ========== CONFIGURATION ==========
APP_KEY = os.getenv("TFL_APP_KEY", "dadde14c06a0411fadfe6060a20e1b85")

if not APP_KEY:
    raise ValueError("Missing TfL app key. Set with: export TFL_APP_KEY='your_key_here'")

BASE_URL = "https://api.tfl.gov.uk"

# Define data directories relative to repo root
ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "tfl" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "tfl" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ========== FETCH FUNCTIONS ==========
def fetch(endpoint: str):
    """Generic GET wrapper with key param."""
    params = {"app_key": APP_KEY, "stripContent": "true"}
    url = f"{BASE_URL}{endpoint}"
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_disruptions():
    """Live disruptions/incidents."""
    return fetch("/Road/all/Disruption")


def fetch_status():
    """High-level congestion status per road."""
    return fetch("/Road/all/Status")


# ========== NORMALIZATION ==========
def normalize_disruption(d):
    """Simplify disruption record."""
    lat, lon = None, None
    try:
        text = (
            d.get("geometry", {})
            .get("geography", {})
            .get("wellKnownText", "")
        )
        if text.startswith("POINT("):
            lon, lat = map(float, text.strip("POINT()").split())
    except Exception:
        pass

    return {
        "record_type": "disruption",
        "id": d.get("id"),
        "roadIds": d.get("roadIds"),
        "corridorIds": d.get("corridorIds"),
        "category": d.get("category"),
        "subCategory": d.get("subCategory"),
        "severity": d.get("severity"),
        "currentUpdate": d.get("currentUpdate"),
        "comments": d.get("comments"),
        "status": d.get("status"),
        "levelOfInterest": d.get("levelOfInterest"),
        "startDateTime": d.get("startDateTime"),
        "endDateTime": d.get("endDateTime"),
        "location": d.get("location"),
        "lat": lat,
        "lon": lon,
        "hasClosures": d.get("hasClosures"),
        "source": "tfl_api",
    }


def normalize_status(s):
    """Simplify per-road status record."""
    return {
        "record_type": "status",
        "id": s.get("id"),
        "display_name": s.get("displayName"),
        "status_severity": s.get("statusSeverity"),
        "status_description": s.get("statusSeverityDescription"),
        "bounds": s.get("bounds"),
        "envelope": s.get("envelope"),
        "source": "tfl_api",
    }


# ========== MAIN ==========
def main():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    print(f"[*] Starting TfL extraction ({timestamp})")

    # ---- Step 1: Fetch raw data ----
    print("[*] Fetching TfL disruptions…")
    disruptions = fetch_disruptions()
    print(f"    → {len(disruptions)} records")

    print("[*] Fetching TfL road status…")
    status = fetch_status()
    print(f"    → {len(status)} records")

    # ---- Step 2: Save raw dumps ----
    raw_disruptions_path = RAW_DIR / f"tfl_disruptions_{timestamp}.json"
    raw_status_path = RAW_DIR / f"tfl_status_{timestamp}.json"

    with open(raw_disruptions_path, "w") as f:
        json.dump(disruptions, f, indent=2)
    with open(raw_status_path, "w") as f:
        json.dump(status, f, indent=2)

    print(f"[+] Raw JSON saved under {RAW_DIR}")

    # ---- Step 3: Normalize + merge ----
    combined = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "disruptions": len(disruptions),
            "status": len(status),
        },
        "data": {
            "disruptions": [normalize_disruption(d) for d in disruptions],
            "status": [normalize_status(s) for s in status],
        },
    }

    processed_path = PROCESSED_DIR / f"tfl_combined_{timestamp}.json"
    with open(processed_path, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"[+] Combined processed JSON saved → {processed_path}")
    print(json.dumps(combined["summary"], indent=2))
    print("[✓] TfL extraction complete.")


if __name__ == "__main__":
    main()
