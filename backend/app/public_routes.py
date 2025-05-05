from datetime import date

from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Request

from . import crud, schemas
from .database import get_db

public_router = APIRouter()
templates = Jinja2Templates(directory="/frontend/templates")


@public_router.get("/track/{tracking_number}", response_model=schemas.LocationResponse)
def get_location(tracking_number: str, db: Session = Depends(get_db)):
    today = date.today()

    tracker = crud.get_location_by_date(db, tracking_number, today)

    if not tracker:
        tracker = crud.get_closest_location_to_date(db, tracking_number, today)

        if not tracker:
            raise HTTPException(status_code=404, detail="Not found")

    return tracker


@public_router.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
