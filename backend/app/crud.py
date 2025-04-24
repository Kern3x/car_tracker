from . import models
from sqlalchemy.orm import Session


def get_all_locations(db: Session):
    return db.query(models.Location).all()


def get_location_by_track_number(db: Session, track_number: str):
    return (
        db.query(models.Location)
        .filter(models.Location.tracking_number == track_number)
        .first()
    )


def create_location(db: Session, location):
    db_location = models.Location(
        tracking_number=location.tracking_number,
        latitude=location.latitude,
        longitude=location.longitude,
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(db: Session, location: models.Location):
    db.query(models.Location).filter(
        models.Location.tracking_number == location.tracking_number
    ).update(
        {
            models.Location.latitude: location.latitude,
            models.Location.longitude: location.longitude,
        }
    )
    db.commit()


def delete_location(db: Session, track_number: str):
    location = (
        db.query(models.Location)
        .filter(models.Location.tracking_number == track_number)
        .first()
    )
    if location:
        db.delete(location)
        db.commit()
    return location
