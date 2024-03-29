from typing import Optional

import pymongo
from beanie import Document, Indexed


class Category(Document):
    name: str
    description: str

    class Settings:
        name = "category"


class Event(Document):
    title: Indexed(str, index_type=pymongo.TEXT, unique=True)
    description: Optional[Indexed(str, index_type=pymongo.TEXT)] = None
    address: Optional[Indexed(str, index_type=pymongo.TEXT)] = None
    category_id: str

    class Settings:
        name = "event"
