from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from app.database import Base

class TrafficStatus(Base):
    __tablename__ = "traffic_status"

    id = Column(String, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("etl_runs.id", ondelete="CASCADE"))
    display_name = Column(String)
    status_severity = Column(String)
    status_description = Column(String)
    bounds = Column(String)
    envelope = Column(String)
    source = Column(String)
