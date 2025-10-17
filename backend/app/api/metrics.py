from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.traffic_disruption import TrafficDisruption
from app.models.traffic_status import TrafficStatus

router = APIRouter(prefix="/traffic", tags=["Traffic Metrics"])

@router.get("/metrics")
def get_traffic_metrics(db: Session = Depends(get_db)):
    """Compute summarized traffic metrics for UI visualization."""

    status_records = db.query(TrafficStatus).all()
    disruptions = db.query(TrafficDisruption).all()

    total_roads = len(status_records)
    if total_roads == 0:
        return {
            "congestion_percentage": 0,
            "average_delay_minutes": 0,
            "journey_time_with_traffic": 0,
            "journey_time_without_traffic": 0,
            "incidents_detected": 0,
            "traffic_speed_kmh": 0,
        }

    congested_roads = sum(1 for r in status_records if r.status_severity.lower() != "good")
    congestion_percentage = round((congested_roads / total_roads) * 100, 2)

    delay_map = {
        "Good": 0, "Minor": 5, "Moderate": 10,
        "Serious": 15, "Closure": 20
    }
    avg_delay = round(
        sum(delay_map.get(r.status_severity, 0) for r in status_records) / total_roads, 2
    )

    incidents_detected = len(disruptions)

    journey_time_without_traffic = 30  # minutes baseline
    journey_time_with_traffic = round(
        journey_time_without_traffic * (1 + (congestion_percentage / 100) * 0.4), 1
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
