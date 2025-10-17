from pydantic import BaseModel
from typing import Optional, List

class Disruption(BaseModel):
    id: str
    category: Optional[str]
    severity: Optional[str]
    location: Optional[str]
    lat: Optional[float]
    lon: Optional[float]

    class Config:
        orm_mode = True


class Status(BaseModel):
    id: str
    display_name: Optional[str]
    status_severity: Optional[str]
    status_description: Optional[str]

    class Config:
        orm_mode = True


class Summary(BaseModel):
    total_disruptions: int
    total_status: int
