from database import get_database
from motor.motor_asyncio import AsyncIOMotorClient


async def get_db_client() -> AsyncIOMotorClient:
    db = get_database()
    try:
        yield db
    finally:
        pass
