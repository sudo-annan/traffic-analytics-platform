#!/usr/bin/env python3
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
    data_dir = Path(__file__).resolve().parents[2] / "data" / "google" / "processed"
    files = sorted(data_dir.glob("combined_*.json"), key=lambda f: f.stat().st_mtime)
    if not files:
        print("No Google traffic JSON found.")
        return

    latest = files[-1]
    print(f"[*] Loading {latest.name}")
    payload = load_json(latest)

    conn = connect_db()
    cur = conn.cursor()

    # --- Ensure tables exist ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS etl_runs (
            id SERIAL PRIMARY KEY,
            run_timestamp TIMESTAMPTZ DEFAULT NOW(),
            source TEXT,
            city TEXT,
            total_routes INT,
            congestion_percentage NUMERIC,
            average_delay_minutes NUMERIC
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS google_traffic_data (
            id SERIAL PRIMARY KEY,
            run_id INT REFERENCES etl_runs(id) ON DELETE CASCADE,
            city TEXT,
            lat DOUBLE PRECISION,
            lon DOUBLE PRECISION,
            route_name TEXT,
            timestamp TIMESTAMPTZ,
            congestion_percentage NUMERIC,
            average_delay_minutes NUMERIC,
            traffic_level TEXT,
            red_percentage NUMERIC,
            yellow_percentage NUMERIC,
            green_percentage NUMERIC,
            screenshot_path TEXT,
            extraction_method TEXT,
            extraction_timestamp TIMESTAMPTZ
        );
    """)

    # --- Insert route data ---
    results = payload.get("results", [])
    total_routes = len(results)
    if total_routes == 0:
        print("No routes found in payload.")
        return

    # Compute aggregate metrics
    avg_congestion = sum(r["congestion_percentage"] for r in results) / total_routes
    avg_delay = sum(r["average_delay_minutes"] for r in results) / total_routes

    # Insert ETL run summary
    cur.execute("""
        INSERT INTO etl_runs (source, city, total_routes, congestion_percentage, average_delay_minutes)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """, ("google", payload["city"], total_routes, avg_congestion, avg_delay))
    run_id = cur.fetchone()[0]

    # Insert each route record linked to the run
    for entry in results:
        cur.execute("""
            INSERT INTO google_traffic_data (
                run_id, city, lat, lon, route_name,
                congestion_percentage, average_delay_minutes, traffic_level,
                red_percentage, yellow_percentage, green_percentage,
                extraction_method, screenshot_path, timestamp, extraction_timestamp
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            run_id,
            payload["city"],
            float(entry["location"].split(",")[0]),
            float(entry["location"].split(",")[1]),
            entry.get("route_name"),
            entry.get("congestion_percentage"),
            entry.get("average_delay_minutes"),
            entry.get("traffic_level"),
            entry["color_breakdown"].get("red"),
            entry["color_breakdown"].get("yellow"),
            entry["color_breakdown"].get("green"),
            entry.get("extraction_method"),
            entry.get("screenshot_path"),
            datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")),
            datetime.fromisoformat(payload["extraction_timestamp"].replace("Z", "+00:00")),
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"[+] Inserted {total_routes} records into google_traffic_data (Run ID {run_id}).")

if __name__ == "__main__":
    main()
