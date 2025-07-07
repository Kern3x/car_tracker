from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from datetime import datetime


def get_all_locations(db: Session):
    return db.query(models.Location).all()


def get_location_by_track_number(db: Session, track_number: str):
    return (
        db.query(models.Location)
        .filter(models.Location.tracking_number == track_number)
        .order_by(models.Location.timestamp.desc())
        .first()
    )


def get_location_by_id(db: Session, _id: int):
    return db.query(models.Location).filter(models.Location.id == _id).first()
    

def get_location_by_date(db: Session, track_number: str, date: datetime):
    return (
        db.query(models.Location)
        .filter(models.Location.tracking_number == track_number)
        .order_by(func.abs(func.extract("epoch", models.Location.timestamp - date)))
        .first()
    )


def get_closest_location_to_date(
    db: Session, tracking_number: str, target_date: datetime
):
    return (
        db.query(models.Location)
        .filter(models.Location.tracking_number == tracking_number)
        .order_by(
            func.abs(func.extract("epoch", models.Location.timestamp - target_date))
        )
        .first()
    )


def create_location(db: Session, location):
    db_location = models.Location(
        tracking_number=location.tracking_number,
        latitude=location.latitude,
        longitude=location.longitude,
        timestamp=location.timestamp or datetime.utcnow(),
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def delete_locations_by_track_number(db: Session, track_number: str) -> int:
    deleted = (
        db.query(models.Location)
        .filter(models.Location.tracking_number == track_number)
        .delete()
    )
    db.commit()
    return deleted
