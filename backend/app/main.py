from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .admin_routes import admin_router
from .public_routes import public_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(public_router)
app.include_router(admin_router, prefix="/admin")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можна обмежити список дозволених доменів
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
