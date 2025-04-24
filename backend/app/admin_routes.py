from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/set-location", response_model=schemas.TrackerOut)
def set_location(tracker: schemas.TrackerCreate, db: Session = Depends(get_db)):
    return crud.create_or_update_tracker(db, tracker)
