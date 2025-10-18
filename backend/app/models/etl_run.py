from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric
from app.database import Base

class EtlRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_timestamp = Column(TIMESTAMP)
    source = Column(String)
    city = Column(String)
    total_routes = Column(Integer)
    congestion_percentage = Column(Numeric)
    average_delay_minutes = Column(Numeric)
