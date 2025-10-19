from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.google_traffic import GoogleTrafficData
from app.models.weather import WeatherData
from app.models.etl_run import EtlRun

router = APIRouter(prefix="/traffic", tags=["Traffic"])

@router.get("/summary")
def get_summary(city: str = Query(...), db: Session = Depends(get_db)):
    # latest run for city
    latest = db.query(EtlRun).filter(EtlRun.city==city).order_by(EtlRun.run_timestamp.desc()).first()
    if not latest:
        return {"message":"No data"}
    # fetch latest weather
    weather = db.query(WeatherData).filter(WeatherData.city==city).order_by(WeatherData.timestamp.desc()).first()
    return {
        "run_id": latest.id,
        "run_timestamp": latest.run_timestamp,
        "total_routes": latest.total_routes,
        "congestion_percentage": float(latest.congestion_percentage or 0),
        "average_delay_minutes": float(latest.average_delay_minutes or 0),
        "weather": {
            "temp_c": float(weather.temp_c) if weather else None,
            "condition": weather.condition if weather else None,
            "humidity": float(weather.humidity) if weather else None
        }
    }

@router.get("/history")
def get_history(city: str = Query(...), db: Session = Depends(get_db)):
    runs = db.query(EtlRun).filter(EtlRun.city==city).order_by(EtlRun.run_timestamp.asc()).all()
    out = []
    for r in runs:
        out.append({
            "timestamp": r.run_timestamp,
            "congestion_percentage": float(r.congestion_percentage or 0),
            "average_delay_minutes": float(r.average_delay_minutes or 0)
        })
    return out
