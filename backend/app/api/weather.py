from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.weather import WeatherData

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current")
def get_current_weather(db: Session = Depends(get_db)):
    latest = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).first()
    if not latest:
        return {"message": "No weather data available."}
    return {
        "timestamp": latest.timestamp,
        "temp_c": float(latest.temp_c),
        "condition": latest.condition,
        "wind_kph": float(latest.wind_kph),
        "humidity": float(latest.humidity),
        "cloud": float(latest.cloud),
        "pressure_mb": float(latest.pressure_mb),
        "feelslike_c": float(latest.feelslike_c),
        "precip_mm": float(latest.precip_mm),
        "uv": float(latest.uv),
    }
