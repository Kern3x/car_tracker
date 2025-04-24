from sqlalchemy.orm import Session
from . import models, schemas

def get_tracker(db: Session, tracking_number: str):
    return db.query(models.CarTracker).filter(models.CarTracker.tracking_number == tracking_number).first()

def create_or_update_tracker(db: Session, tracker: schemas.TrackerCreate):
    db_tracker = get_tracker(db, tracker.tracking_number)
    if db_tracker:
        db_tracker.latitude = tracker.latitude
        db_tracker.longitude = tracker.longitude
    else:
        db_tracker = models.CarTracker(**tracker.dict())
        db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker
