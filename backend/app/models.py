from sqlalchemy import Column, String, Float
from .database import Base

class CarTracker(Base):
    __tablename__ = "car_trackers"

    tracking_number = Column(String(26), primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
