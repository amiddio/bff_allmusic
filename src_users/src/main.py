from fastapi import FastAPI

from databases.mongodb import connect_to_mongodb, close_mongodb_connection
from models.settings import Settings
from routes.v1.api import router as api_router

app = FastAPI()

app.add_event_handler('startup', connect_to_mongodb)
app.add_event_handler('shutdown', close_mongodb_connection)

app.include_router(api_router, prefix=Settings().API_URI_PREFIX)
