from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, ARRAY, ForeignKey
from app.database import Base

class TrafficDisruption(Base):
    __tablename__ = "traffic_disruptions"

    id = Column(String, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("etl_runs.id", ondelete="CASCADE"))
    category = Column(String)
    sub_category = Column(String)
    severity = Column(String)
    current_update = Column(String)
    comments = Column(String)
    status = Column(String)
    level_of_interest = Column(String)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    location = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    has_closures = Column(Boolean)
    road_ids = Column(ARRAY(String))
    corridor_ids = Column(ARRAY(String))
    source = Column(String)
