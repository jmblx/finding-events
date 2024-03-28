from typing import Optional

import pymongo
from beanie import Document


class Category(Document):
    name: str
    description: str

    class Settings:
        name = "category"


class Event(Document):
    title: str
    description: Optional[str] = None
    address: Optional[str] = None
    category_id: str

    class Settings:
        name = "event"
        indexes = [
            [
                ("title", pymongo.TEXT),
                ("description", pymongo.TEXT),
            ]
        ]
