from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

public_router = APIRouter()


@public_router.get("/track/{tracking_number}", response_model=schemas.TrackerOut)
def get_location(tracking_number: str, db: Session = Depends(get_db)):
    tracker = crud.get_location_by_track_number(db, tracking_number)

    if not tracker:
        raise HTTPException(status_code=404, detail="Not found")

    return tracker
