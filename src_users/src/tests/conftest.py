import asyncio
import httpx
import pytest
import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from main import app
from models.settings import Settings
from models.subscriber import Subscriber
from models.user import User, UserRegister

settings = Settings()


@pytest_asyncio.fixture(scope="session")
async def db() -> None:
    MONGODB_TEST_DB = settings.MONGODB_DB + '_test'
    url = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASS}@" \
          f"{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"

    ac = AsyncIOMotorClient(
        url,
        maxPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT,
        minPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT
    )
    ac.get_io_loop = asyncio.get_event_loop
    await init_beanie(
        database=ac.get_database(MONGODB_TEST_DB),
        document_models=[User, UserRegister, Subscriber]
    )


@pytest_asyncio.fixture(scope="session")
async def client(db):
    async with httpx.AsyncClient(app=app, base_url=f"http://web-app-users{settings.API_URI_PREFIX}") as ac:
        yield ac
        await User.find_all().delete()
