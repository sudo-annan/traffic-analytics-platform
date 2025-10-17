#!/usr/bin/env python3
"""
etl_tfl_loader.py
Load normalized TfL combined JSON (disruptions + status) into PostgreSQL.
Also computes and stores summary traffic metrics for each ETL run.
"""

import json
import psycopg2
from pathlib import Path
from statistics import mean
from datetime import datetime, timezone

# --- DB CONFIG ---
DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "traffic_db",
    "user": "traffic_user",
    "password": "traffic_pass",
}

# --- DATABASE UTILS ---
def connect_db():
    return psycopg2.connect(**DB)


def insert_etl_run(cur, summary, metrics):
    cur.execute(
        """
        INSERT INTO etl_runs (
            run_timestamp,
            total_disruptions,
            total_status,
            congestion_percentage,
            average_delay_minutes,
            journey_time_with_traffic,
            journey_time_without_traffic,
            incidents_detected,
            traffic_speed_kmh
        )
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            summary.get("disruptions"),
            summary.get("status"),
            metrics["congestion_percentage"],
            metrics["average_delay_minutes"],
            metrics["journey_time_with_traffic"],
            metrics["journey_time_without_traffic"],
            metrics["incidents_detected"],
            metrics["traffic_speed_kmh"],
        ),
    )
    return cur.fetchone()[0]


def insert_disruptions(cur, disruptions, run_id):
    for d in disruptions:
        cur.execute(
            """
            INSERT INTO traffic_disruptions (
                id, run_id, category, sub_category, severity, current_update,
                comments, status, level_of_interest, start_time, end_time,
                location, lat, lon, has_closures, road_ids, corridor_ids, source
            )
            VALUES (
                %(id)s, %(run_id)s, %(category)s, %(subCategory)s, %(severity)s,
                %(currentUpdate)s, %(comments)s, %(status)s, %(levelOfInterest)s,
                %(startDateTime)s, %(endDateTime)s, %(location)s, %(lat)s, %(lon)s,
                %(hasClosures)s, %(roadIds)s, %(corridorIds)s, %(source)s
            )
            ON CONFLICT (id) DO NOTHING;
            """,
            {**d, "run_id": run_id},
        )


def insert_status(cur, status, run_id):
    for s in status:
        cur.execute(
            """
            INSERT INTO traffic_status (
                id, run_id, display_name, status_severity, status_description,
                bounds, envelope, source
            )
            VALUES (
                %(id)s, %(run_id)s, %(display_name)s, %(status_severity)s,
                %(status_description)s, %(bounds)s, %(envelope)s, %(source)s
            )
            ON CONFLICT (id) DO NOTHING;
            """,
            {**s, "run_id": run_id},
        )


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# --- METRICS CALCULATION ---
def compute_metrics(disruptions, status):
    total_roads = len(status)
    incidents_detected = len(disruptions)

    if total_roads == 0:
        return {
            "congestion_percentage": 0,
            "average_delay_minutes": 0,
            "journey_time_with_traffic": 0,
            "journey_time_without_traffic": 0,
            "incidents_detected": incidents_detected,
            "traffic_speed_kmh": 0,
        }

    congested_roads = sum(1 for r in status if r.get("status_severity", "").lower() != "good")
    congestion_percentage = round((congested_roads / total_roads) * 100, 2)

    delay_map = {"Good": 0, "Minor": 5, "Moderate": 10, "Serious": 15, "Closure": 20}
    avg_delay = round(
        mean([delay_map.get(r.get("status_severity"), 0) for r in status]), 2
    )

    journey_time_without_traffic = 30  # baseline minutes
    journey_time_with_traffic = round(
        journey_time_without_traffic * (1 + congestion_percentage / 100 * 0.4), 1
    )
    traffic_speed_kmh = round(max(10, 60 * (1 - congestion_percentage / 100)), 1)

    return {
        "congestion_percentage": congestion_percentage,
        "average_delay_minutes": avg_delay,
        "journey_time_with_traffic": journey_time_with_traffic,
        "journey_time_without_traffic": journey_time_without_traffic,
        "incidents_detected": incidents_detected,
        "traffic_speed_kmh": traffic_speed_kmh,
    }


# --- MAIN ETL PROCESS ---
def main():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "tfl" / "processed"
    files = sorted(data_dir.glob("tfl_combined_*.json"))
    if not files:
        print("No processed TfL JSON found in data/tfl/processed/.")
        return

    latest = files[-1]
    print(f"[*] Loading {latest.name}")
    payload = load_json(latest)

    disruptions = payload["data"]["disruptions"]
    status = payload["data"]["status"]
    summary = payload["summary"]

    # Compute metrics
    metrics = compute_metrics(disruptions, status)
    print("[*] Metrics computed:")
    print(json.dumps(metrics, indent=2))

    # DB operations
    conn = connect_db()
    cur = conn.cursor()

    run_id = insert_etl_run(cur, summary, metrics)
    print(f"[*] Run ID {run_id}")

    insert_disruptions(cur, disruptions, run_id)
    insert_status(cur, status, run_id)

    conn.commit()
    cur.close()
    conn.close()
    print(f"[+] ETL completed: {len(disruptions)} disruptions, {len(status)} status, run {run_id}")


if __name__ == "__main__":
    main()