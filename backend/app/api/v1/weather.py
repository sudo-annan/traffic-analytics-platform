from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.weather import WeatherData

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current")
def get_current(city: str = Query(...), db: Session = Depends(get_db)):
    latest = db.query(WeatherData).filter(WeatherData.city==city).order_by(WeatherData.timestamp.desc()).first()
    if not latest:
        return {"message":"No weather data"}
    return {
        "timestamp": latest.timestamp,
        "temp_c": float(latest.temp_c),
        "condition": latest.condition,
        "humidity": float(latest.humidity)
    }
