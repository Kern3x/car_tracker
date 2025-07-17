from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .admin_routes import admin_router
from .public_routes import public_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(public_router)
app.include_router(admin_router)

allow_origins=["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # List of restricted domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="/frontend/static"), name="static")
