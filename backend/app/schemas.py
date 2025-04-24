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
