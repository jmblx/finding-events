from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from event.db import Db
from event.models import Event

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/pages", tags=["pages"])

db = Db()


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    events = await db.get_all(Event)
    return templates.TemplateResponse("index.html", {"request": request, "events": events})
