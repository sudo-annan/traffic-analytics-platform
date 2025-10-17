#!/usr/bin/env python3
"""
etl_weather_loader.py
Load processed WeatherAPI data into PostgreSQL.
"""

import json
import psycopg2
from pathlib import Path
from datetime import datetime

DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "traffic_db",
    "user": "traffic_user",
    "password": "traffic_pass",
}

def connect_db():
    return psycopg2.connect(**DB)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "weather" / "processed"
    files = sorted(data_dir.glob("weather_*.json"))
    if not files:
        print("No weather JSON found.")
        return

    latest = files[-1]
    print(f"[*] Loading {latest.name}")
    weather = load_json(latest)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            location TEXT,
            country TEXT,
            temp_c NUMERIC,
            condition TEXT,
            wind_kph NUMERIC,
            humidity NUMERIC,
            cloud NUMERIC,
            pressure_mb NUMERIC,
            feelslike_c NUMERIC,
            precip_mm NUMERIC,
            uv NUMERIC
        );
        """
    )

    cur.execute(
        """
        INSERT INTO weather_data (
            timestamp, location, country, temp_c, condition, wind_kph, humidity,
            cloud, pressure_mb, feelslike_c, precip_mm, uv
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        );
        """,
        (
            datetime.fromisoformat(weather["timestamp"]),
            weather["location"],
            weather["country"],
            weather["temp_c"],
            weather["condition"],
            weather["wind_kph"],
            weather["humidity"],
            weather["cloud"],
            weather["pressure_mb"],
            weather["feelslike_c"],
            weather["precip_mm"],
            weather["uv"],
        ),
    )

    conn.commit()
    cur.close()
    conn.close()
    print("[+] Weather data inserted into DB.")

if __name__ == "__main__":
    main()
