from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from event.db import Db
from event.models import Event, Category

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/pages", tags=["pages"])

db = Db()


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    events = await db.get_all(Event)
    return templates.TemplateResponse("index.html", {"request": request, "events": events})


@router.get("/category/{category_id}", response_class=HTMLResponse)
async def category_events_page(request: Request, category_id: str):
    events = await db.get(Event, criteria={"category_id": category_id})
    categories_dict = await db.get_categories_dict()
    category_name = categories_dict.get(category_id, "Unknown Category")
    return templates.TemplateResponse(
        "category.html", {
            "request": request, "events": events, "category_name": category_name, "categories_dict": categories_dict
        }
    )


@router.get("/event/{event_id}", response_class=HTMLResponse)
async def event_details_page(request: Request, event_id: str):
    event = await db.get_one(Event, criteria={"_id": ObjectId(event_id)})
    return templates.TemplateResponse("event_details.html", {"request": request, "event": event})


@router.get("/new_event", response_class=HTMLResponse)
async def add_event_page(request: Request):
    return templates.TemplateResponse("add_event.html", {"request": request, "categories": await db.get_all(Category)})
