from typing import List, Optional
from beanie import Document, Indexed, Link, BackLink
import pymongo
from pydantic import Field


class Event(Document):
    title: Indexed(str, index_type=pymongo.TEXT, unique=True)
    description: Optional[Indexed(str, index_type=pymongo.TEXT)] = None
    img_path: Optional[str]
    address: Optional[Indexed(str, index_type=pymongo.TEXT)] = None
    category: Link["Category"]

    class Settings:
        name = "event"


class Category(Document):
    name: str
    description: str

    events: List[BackLink[Event]] = Field(original_field="category")

    class Settings:
        name = "category"
