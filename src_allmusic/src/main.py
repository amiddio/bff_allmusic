from fastapi import FastAPI

from database.database import Base, engine
from schemas.settings import Settings
from routes.v1.api import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=Settings().API_URI_PREFIX)
