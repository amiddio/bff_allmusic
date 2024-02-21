from fastapi import FastAPI

from schemas.settings import Settings
from routes.v1.api import router as api_router


app = FastAPI()

app.include_router(api_router, prefix=Settings().API_URI_PREFIX)
