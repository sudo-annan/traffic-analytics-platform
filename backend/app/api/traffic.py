from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.traffic_disruption import TrafficDisruption
from app.models.traffic_status import TrafficStatus
from app.models.etl_run import EtlRun
from app.schemas.traffic_schema import Disruption, Status
from app.services.tfl_refresh import refresh_tfl_data

router = APIRouter(prefix="/traffic", tags=["Traffic"])


@router.get("/disruptions", response_model=list[Disruption])
def get_disruptions(db: Session = Depends(get_db)):
    return db.query(TrafficDisruption).order_by(TrafficDisruption.id.desc()).limit(50).all()


@router.get("/status", response_model=list[Status])
def get_status(db: Session = Depends(get_db)):
    return db.query(TrafficStatus).order_by(TrafficStatus.id.desc()).limit(50).all()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Returns the latest ETL run summary including computed metrics.
    """
    latest_run = db.query(EtlRun).order_by(EtlRun.run_timestamp.desc()).first()
    if not latest_run:
        return {
            "message": "No ETL runs found.",
            "total_disruptions": 0,
            "total_status": 0,
            "congestion_percentage": 0,
            "average_delay_minutes": 0,
            "journey_time_with_traffic": 0,
            "journey_time_without_traffic": 0,
            "incidents_detected": 0,
            "traffic_speed_kmh": 0,
        }

    return {
        "run_id": latest_run.id,
        "run_timestamp": latest_run.run_timestamp,
        "total_disruptions": latest_run.total_disruptions,
        "total_status": latest_run.total_status,
        "congestion_percentage": float(latest_run.congestion_percentage or 0),
        "average_delay_minutes": float(latest_run.average_delay_minutes or 0),
        "journey_time_with_traffic": float(latest_run.journey_time_with_traffic or 0),
        "journey_time_without_traffic": float(latest_run.journey_time_without_traffic or 0),
        "incidents_detected": latest_run.incidents_detected or 0,
        "traffic_speed_kmh": float(latest_run.traffic_speed_kmh or 0),
    }


@router.post("/refresh")
def refresh_data():
    """Trigger data refresh from TfL extractor + ETL."""
    success, msg = refresh_tfl_data()
    return {"success": success, "message": msg}


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    runs = db.query(EtlRun).order_by(EtlRun.run_timestamp.asc()).all()
    return [
        {
            "timestamp": r.run_timestamp,
            "congestion_percentage": float(r.congestion_percentage or 0),
            "average_delay_minutes": float(r.average_delay_minutes or 0),
            "traffic_speed_kmh": float(r.traffic_speed_kmh or 0),
        }
        for r in runs
    ]
