from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, Request

from . import crud
from .database import get_db
from .schemas import Location, LocationResponse


admin_router = APIRouter()
templates = Jinja2Templates(directory="/frontend/templates")


@admin_router.get("/", response_class=HTMLResponse)
async def get_admin_page(request: Request, db: Session = Depends(get_db)):
    locations = crud.get_all_locations(db)
    return templates.TemplateResponse("admin.html", {"request": request, "locations": locations})


@admin_router.get("/locations", response_model=List[LocationResponse])
async def get_locations(db: Session = Depends(get_db)):
    locations = crud.get_all_locations(db)
    return locations


@admin_router.post("/set-location", response_model=LocationResponse)
async def set_location(location: Location, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_track_number(
        db, track_number=location.tracking_number
    )

    if db_location:
        raise HTTPException(
            status_code=400, detail="Location for this track number already exists"
        )

    db_location = crud.create_location(db, location=location)

    return LocationResponse(
        id=db_location.id,
        tracking_number=db_location.tracking_number,
        latitude=db_location.latitude,
        longitude=db_location.longitude,
    )


@admin_router.put("/edit-location", response_model=LocationResponse)
async def edit_location(location: Location, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_track_number(
        db, track_number=location.tracking_number
    )
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    db_location.latitude = location.latitude
    db_location.longitude = location.longitude

    db.commit()
    db.refresh(db_location)

    return db_location


@admin_router.delete("/delete-location", response_model=LocationResponse)
async def delete_location(tracking_number: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_track_number(db, track_number=tracking_number)

    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(db_location)
    db.commit()

    return db_location
