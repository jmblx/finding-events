import pymongo
from beanie import Document


class User(Document):
    username: str
    email: str
    full_name: str
    disabled: bool = False

    class Settings:
        name = "user"

        indexes = [
            [
                ("username", pymongo.TEXT),
            ]
        ]
