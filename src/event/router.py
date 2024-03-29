from bson import ObjectId
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


from event.db import Db
from event.models import Event, Category
from event.schemas import EventAdd, CategoryAdd, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])

db = Db()


@router.post("/category")
async def add_category(data: CategoryAdd):
    return await db.add_one(Category, data)


@router.get("/categories")
async def get_categories(response: Response):
    all_categories = await db.get_all(Category)
    return {"data": all_categories}


@router.post("/")
async def add_event(data: EventAdd, response: Response):
    res = await db.add_one(Event, data)
    if "error" in res.keys():
        response.status_code = HTTP_404_NOT_FOUND
    return res


@router.get("/{event_id}")
async def get_event(event_id: str, response: Response):
    print(event_id)
    data = await db.get_one(Event, Event.id == ObjectId(event_id))
    if data.get("error"):
        response.status_code = HTTP_404_NOT_FOUND
        return {"status": data.get("error")}
    return data


@router.get("/")
async def get_all_events():
    return {"data": await db.get_all(Event)}





@router.put("/{event_id}")
async def update_event(event_id: str, data: EventUpdate, response: Response):
    res = await db.update(Event, Event.id == ObjectId(event_id), data)
    if type(res) == dict:
        if "error" in res.keys():
            response.status_code = HTTP_404_NOT_FOUND
            return {"status": res.get("error")}
    return {"status": "ok"}


@router.delete("/{event_id}")
async def delete_event(event_id: str, response: Response):
    res = await db.delete_one(Event, Event.id == ObjectId(event_id))
    if "error" in res.keys():
        response.status_code = HTTP_404_NOT_FOUND
    return res

