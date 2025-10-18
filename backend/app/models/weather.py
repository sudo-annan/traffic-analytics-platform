from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Numeric, ForeignKey
from app.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("etl_runs.id", ondelete="CASCADE"))
    city = Column(String)
    region = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(TIMESTAMP)
    temp_c = Column(Numeric)
    condition = Column(String)
    wind_kph = Column(Numeric)
    humidity = Column(Numeric)
    cloud = Column(Numeric)
    pressure_mb = Column(Numeric)
    feelslike_c = Column(Numeric)
    precip_mm = Column(Numeric)
    uv = Column(Numeric)
