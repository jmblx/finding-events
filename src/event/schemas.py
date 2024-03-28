from typing import Optional

from pydantic import BaseModel


class CategoryAdd(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryGet(CategoryAdd):
    _id: str


class EventAdd(BaseModel):
    title: str
    description: str
    address: str
    category_id: str


class EventUpdate(EventAdd):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    category_id: Optional[str] = None


class EventGet(EventAdd):
    _id: str
