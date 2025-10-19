#!/usr/bin/env python3
"""
etl_weather_loader.py
Load processed WeatherAPI data into PostgreSQL.
"""
import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

# DB = {
#     "host": "localhost",
#     "port": 5432,
#     "dbname": "traffic_db",
#     "user": "traffic_user",
#     "password": "traffic_pass",
# }

# def connect_db():
#     return psycopg2.connect(**DB)

def connect_db():
    DB = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "trafficdb"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASS", "postgres"),
    }
    return psycopg2.connect(**DB)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "weather" / "processed"
    files = sorted(data_dir.glob("weather_*.json"), key=lambda f: f.stat().st_mtime)
    if not files:
        print("No weather JSON found.")
        return

    latest = files[-1]
    print(f"[*] Loading {latest.name}")
    weather = load_json(latest)

    conn = connect_db()
    cur = conn.cursor()

    # ✅ Ensure the table exists
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            city TEXT,
            region TEXT,
            country TEXT,
            lat NUMERIC,
            lon NUMERIC,
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

    # ✅ Insert normalized fields
    cur.execute(
        """
        INSERT INTO weather_data (
            timestamp, city, region, country, lat, lon, temp_c, condition,
            wind_kph, humidity, cloud, pressure_mb, feelslike_c, precip_mm, uv
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        );
        """,
        (
            datetime.fromisoformat(weather["timestamp"]),
            weather.get("city"),
            weather.get("region"),
            weather.get("country"),
            weather.get("lat"),
            weather.get("lon"),
            weather.get("temp_c"),
            weather.get("condition"),
            weather.get("wind_kph"),
            weather.get("humidity"),
            weather.get("cloud"),
            weather.get("pressure_mb"),
            weather.get("feelslike_c"),
            weather.get("precip_mm"),
            weather.get("uv"),
        ),
    )

    conn.commit()
    cur.close()
    conn.close()
    print("[+] Weather data inserted into DB.")

if __name__ == "__main__":
    main()
