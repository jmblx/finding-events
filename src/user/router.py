from typing import Any, Annotated

from fastapi import APIRouter, Depends, Header

from user.models import User
from user.schemas import UserResponse, UserAdd


router = APIRouter(prefix="/api", tags=["api"])


@router.post("/users/", response_model=None)
async def create_user(user: UserAdd) -> Any:
    user = User(**user.model_dump())
    await User.insert_one(user)
    return {"username": user.username, "email": user.email}


@router.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str) -> Any:
    user = dict(await User.find_one({"username": username}))
    if user is None:
        return {"error": "User not found"}
    user["id"] = str(user.get("_id"))
    data = UserResponse(**user)
    return data


@router.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}