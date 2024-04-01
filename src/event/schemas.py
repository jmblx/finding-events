from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field, validator, field_validator

from event.models import Event


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
    img_path: Optional[str] = None
    address: str
    category: str


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str = Field(..., description="The unique identifier for the category")
    name: str
    description: str

    @field_validator('id', mode="before")
    def id_to_string(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: str = Field(..., description="The unique identifier for the event")
    title: str
    description: Optional[str] = None
    img_path: Optional[str] = None
    address: Optional[str] = None
    category: CategoryResponse

    @field_validator('id', mode="before")
    def id_to_string(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        from_attributes = True
