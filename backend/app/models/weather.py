from sqlalchemy import Column, Integer, TIMESTAMP, String, Numeric
from app.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP)
    location = Column(String)
    country = Column(String)
    temp_c = Column(Numeric)
    condition = Column(String)
    wind_kph = Column(Numeric)
    humidity = Column(Numeric)
    cloud = Column(Numeric)
    pressure_mb = Column(Numeric)
    feelslike_c = Column(Numeric)
    precip_mm = Column(Numeric)
    uv = Column(Numeric)
