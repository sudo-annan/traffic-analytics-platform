from fastapi import APIRouter, Query
from pathlib import Path
import subprocess, shlex, os, json
from datetime import datetime

router = APIRouter(prefix="/data", tags=["Refresh"])

PROJECT_ROOT = Path(__file__).resolve().parents[4]

@router.post("/refresh")
def refresh_data(city: str = Query(...), lat: float = Query(...), lon: float = Query(...), headless: bool = Query(False)):
    """
    Trigger Google extractor + weather extractor + ETL loaders for given city and lat/lon.
    Synchronous — returns summary after ETL completes.
    """
    try:
        # build commands
        ge = PROJECT_ROOT / "src" / "extractors" / "google_traffic_extract.py"
        we = PROJECT_ROOT / "src" / "extractors" / "weather_extract.py"
        gel = PROJECT_ROOT / "src" / "etl" / "etl_google_loader.py"
        wel = PROJECT_ROOT / "src" / "etl" / "etl_weather_loader.py"

        headless_flag = "--headless" if headless else ""
        # run google extractor
        cmd1 = f"python3 {shlex.quote(str(ge))} --city {shlex.quote(city)} --lat {lat} --lon {lon} {headless_flag}"
        subprocess.run(cmd1, shell=True, check=True)

        # run weather extractor
        cmd2 = f"python3 {shlex.quote(str(we))} --lat {lat} --lon {lon}"
        subprocess.run(cmd2, shell=True, check=True)

        # run etls
        cmd3 = f"python3 {shlex.quote(str(gel))} --city {shlex.quote(city)}"
        subprocess.run(cmd3, shell=True, check=True)

        cmd4 = f"python3 {shlex.quote(str(wel))} --city {shlex.quote(city)}"
        subprocess.run(cmd4, shell=True, check=True)

        # After ETL, load the latest combined summary from DB
        # Instead of direct DB access here we'll read the most recent files saved by ETL loaders or query DB.
        # We'll query DB using psycopg2 for the summary:
        import psycopg2
        DB = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "dbname": os.getenv("DB_NAME", "traffic_db"),
            "user": os.getenv("DB_USER", "traffic_user"),
            "password": os.getenv("DB_PASS", "traffic_pass"),
        }
        conn = psycopg2.connect(**DB)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, run_timestamp, total_routes, congestion_percentage, average_delay_minutes
            FROM etl_runs WHERE city=%s ORDER BY run_timestamp DESC LIMIT 1
        """, (city,))
        row = cur.fetchone()
        summary = {}
        if row:
            summary = {
                "run_id": row[0],
                "run_timestamp": row[1].isoformat(),
                "total_routes": row[2],
                "congestion_percentage": float(row[3]) if row[3] is not None else None,
                "average_delay_minutes": float(row[4]) if row[4] is not None else None
            }
        cur.close()
        conn.close()

        return {"success": True, "city": city, "summary": summary}

    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"Extractor/ETL failed: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
