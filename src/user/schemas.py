from pydantic import BaseModel


class UserAdd(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True