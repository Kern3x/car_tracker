from fastapi import FastAPI
from .database import Base, engine
from .admin_routes import router as admin_router
from .public_routes import router as public_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(public_router)
app.include_router(admin_router, prefix="/admin")
