from datetime import datetime

from pydantic import BaseModel


class TrackerBase(BaseModel):
    tracking_number: str


class TrackerLocation(BaseModel):
    latitude: float
    longitude: float


class TrackerCreate(TrackerBase, TrackerLocation):
    pass


class TrackerOut(TrackerBase, TrackerLocation):
    pass


class Location(BaseModel):
    tracking_number: str
    latitude: float
    longitude: float
    timestamp: datetime | None = None


class LocationResponse(Location):
    id: int

    class Config:
        from_attributes = True
