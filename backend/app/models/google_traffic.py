from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Numeric, ForeignKey
from app.database import Base

class GoogleTrafficData(Base):
    __tablename__ = "google_traffic_data"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("etl_runs.id", ondelete="CASCADE"))
    city = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    route_name = Column(String)
    timestamp = Column(TIMESTAMP)
    congestion_percentage = Column(Numeric)
    average_delay_minutes = Column(Numeric)
    traffic_level = Column(String)
    red_percentage = Column(Numeric)
    yellow_percentage = Column(Numeric)
    green_percentage = Column(Numeric)
    screenshot_path = Column(String)
    extraction_method = Column(String)
    extraction_timestamp = Column(TIMESTAMP)
