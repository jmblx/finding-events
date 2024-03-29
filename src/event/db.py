from typing import List

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from event.schemas import EventAdd, CategoryAdd

from event.models import Event, Category
from event.utils import validate_id


class Db:

    async def add_one(self, model, data: BaseModel) -> dict:
        try:
            obj = model(**data.model_dump())
            if model == Event:
                if not validate_id(obj.category_id):
                    return {"error": "category not found"}
            await model.insert_one(obj)
        except DuplicateKeyError:
            return {"error": "duplicate key"}

        return {"id": str(obj.id)}

    async def get_one(self, model, criteria) -> dict:
        print(criteria)
        obj = await model.find_one(criteria)
        if not obj:
            return {"error": "not found"}
        return dict(obj)

    async def get(self, model, criteria) -> List:
        objs = await model.find(criteria).to_list()
        objs = [dict(obj) for obj in objs]
        return objs

    async def get_all(self, model) -> list:
        res = []
        async for obj in model.find_all():
            obj_dict = dict(obj)
            for key, value in obj_dict.items():
                if isinstance(value, str) and len(value) > 30:
                    obj_dict[key] = value[:30] + "..."
            obj_dict["id"] = str(obj.id)
            res.append(obj_dict)
        return res

    async def get_categories_dict(self) -> dict:
        categories_dict = {}
        categories = await self.get_all(Category)
        for category in categories:
            categories_dict[category["id"]] = category["name"]
        return categories_dict

    async def delete_one(self, model, criteria):
        obj = await model.find_one(criteria)
        if obj:
            await obj.delete()
            return {"status": "deleted"}
        else:
            return {"error": "not found"}

    async def update(self, model, criteria, data):
        if model == Event:
            validate = await validate_id(data.category_id)
            if not validate.get("is_valid"):
                return validate
        res = await model.find_all(criteria).set(data)
        return res
