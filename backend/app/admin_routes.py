from typing import List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets

from . import crud
from .config import config
from .database import get_db
from .schemas import Location, LocationResponse


admin_router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="/frontend/templates")

security = HTTPBasic()

base_conf = config.get("base")


def check_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, base_conf.ADMIN_LOGIN
    )
    correct_password = secrets.compare_digest(
        credentials.password, base_conf.ADMIN_PASSWD
    )

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")


@admin_router.get("/", response_class=HTMLResponse)
async def get_admin_page(
    request: Request,
    db: Session = Depends(get_db),
    _: HTTPBasicCredentials = Depends(check_admin),
):
    locations = crud.get_all_locations(db)
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "locations": locations},
    )


@admin_router.get("/locations", response_model=List[LocationResponse])
async def get_locations(
    db: Session = Depends(get_db),
    _: HTTPBasicCredentials = Depends(check_admin),
):
    return crud.get_all_locations(db)


@admin_router.post("/set-location", response_model=LocationResponse)
async def set_location(
    location: Location,
    db: Session = Depends(get_db),
    _: HTTPBasicCredentials = Depends(check_admin),
):
    return crud.create_location(db, location)


@admin_router.put("/edit-location", response_model=LocationResponse)
async def edit_location(
    location: Location,
    db: Session = Depends(get_db),
    _: HTTPBasicCredentials = Depends(check_admin),
):
    db_location = crud.get_location_by_track_number(
        db, track_number=location.tracking_number
    )
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    db_location.latitude = location.latitude
    db_location.longitude = location.longitude
    db_location.timestamp = location.timestamp

    db.commit()
    db.refresh(db_location)
    return db_location


@admin_router.delete("/delete-location", response_model=LocationResponse)
async def delete_location(
    tracking_number: str,
    db: Session = Depends(get_db),
    _: HTTPBasicCredentials = Depends(check_admin),
):
    db_location = crud.get_location_by_track_number(db, track_number=tracking_number)

    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    deleted = crud.delete_locations_by_track_number(db, track_number=tracking_number)

    return deleted
