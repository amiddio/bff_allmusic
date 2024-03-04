from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.settings import Settings
from models.subscriber import Subscriber
from models.user import UserRegister, User


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def connect_to_mongodb():
    settings = Settings()

    url = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASS}@" \
          f"{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"

    db.client = AsyncIOMotorClient(
        url,
        maxPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT,
        minPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT
    )
    await init_beanie(
        database=db.client.get_database(settings.MONGODB_DB),
        document_models=[
            User, UserRegister, Subscriber
        ]
    )


async def close_mongodb_connection():
    db.client.close()
