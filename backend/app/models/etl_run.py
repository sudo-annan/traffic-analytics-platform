from sqlalchemy import Column, Integer, TIMESTAMP, Numeric
from app.database import Base


class EtlRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_timestamp = Column(TIMESTAMP)
    total_disruptions = Column(Integer)
    total_status = Column(Integer)

    # Newly added metrics columns
    congestion_percentage = Column(Numeric)
    average_delay_minutes = Column(Numeric)
    journey_time_with_traffic = Column(Numeric)
    journey_time_without_traffic = Column(Numeric)
    incidents_detected = Column(Integer)
    traffic_speed_kmh = Column(Numeric)
