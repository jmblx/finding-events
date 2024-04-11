import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from event.models import Category, Event
from user.models import User


class DataBase:
    client: AsyncIOMotorClient = None

    def get_db_client(self) -> AsyncIOMotorClient:
        return self.client


db = DataBase()


def get_database() -> AsyncIOMotorClient:
    return db.get_db_client()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(f'mongodb://{os.getenv("MONGO_HOSTNAME", "localhost")}:27017/{os.getenv("MONGO_DB")}')
    await init_beanie(database=db.client.db_name, document_models=[Category, User, Event])


def close_mongo_connection():
    db.client.close()
