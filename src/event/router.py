import json
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Response, UploadFile, File, Form
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


from event.db import Db
from event.models import Event, Category
from event.schemas import EventAdd, CategoryAdd, EventUpdate, EventResponse, CategoryResponse

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
    event = await db.get_one(Event, Event.id == ObjectId(event_id))
    if event.get("error"):
        response.status_code = HTTP_404_NOT_FOUND
        return {"status": event.get("error")}

    event_response = EventResponse.from_orm(event)
    return event


@router.get("/")
async def get_all_events():
    print(await db.get_all(Event))
    return await db.get_all(Event)


@router.put("/{event_id}")
async def update_event(event_id: str, response: Response, file: Optional[UploadFile] = File(None), data: str = Form(...)):
    data = json.loads(data)
    update_data = EventUpdate(**data)
    res = await db.update(
        model=Event, criteria=Event.id == ObjectId(event_id), update_data=update_data, img=file, obj_id=event_id)
    if type(res) == dict:
        if "error" in res.keys():
            response.status_code = HTTP_404_NOT_FOUND
            return {"status": res.get("error")}
    return res


@router.delete("/{event_id}")
async def delete_event(event_id: str, response: Response):
    res = await db.delete_one(Event, Event.id == ObjectId(event_id))
    if "error" in res.keys():
        response.status_code = HTTP_404_NOT_FOUND
    return res


# @router.put("/{event_id}/")
# async def upload_team_avatar(
#     file: Optional[UploadFile] = File(None),
#     event_id: str,
# ):
#     return {"new_path": await db.set_photo(Event, event_id, file)}
