from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/track/{tracking_number}", response_model=schemas.TrackerOut)
def get_location(tracking_number: str, db: Session = Depends(get_db)):
    tracker = crud.get_tracker(db, tracking_number)
    if not tracker:
        raise HTTPException(status_code=404, detail="Not found")
    return tracker
