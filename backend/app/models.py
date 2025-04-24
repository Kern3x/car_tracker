from sqlalchemy import Column, String, Float, Integer

from .database import Base


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_number = Column(String(26), primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
