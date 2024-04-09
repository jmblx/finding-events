import os
import shutil
from typing import List

from beanie import Link, Document
from bson import ObjectId, DBRef
from bson.errors import InvalidId
from PIL import Image
from pydantic import BaseModel, ValidationError
from pymongo.errors import DuplicateKeyError

from event.schemas import (
    EventUpdate, CategoryResponse, EventResponse
)

from event.models import Event, Category
from event.utils import validate_id


class Db:

    async def add_one(self, model, data: BaseModel) -> dict:
        try:
            data = data.model_dump()
            obj = model(**data)
            if model == Event:
                if not (await validate_id(data.get("category"))).get("is_valid"):
                    return {"error": "category not found"}
        except DuplicateKeyError:
            return {"error": "duplicate key"}
        except ValidationError:
            return {"error": "validation error"}
        await model.insert_one(obj)
        return {"id": str(obj.id)}


    async def get_one(self, model, criteria) -> dict:
        obj = await model.find_one(criteria, fetch_links=True, nesting_depth=1)
        if not obj:
            return {"error": "not found"}
        data = dict(obj)
        return data

    async def get(self, model, criteria) -> List:
        objs = await model.find(criteria, fetch_links=True, nesting_depth=1).to_list()
        objs = [dict(obj) for obj in objs]
        return objs

    async def get_all(self, model) -> list:
        res = []
        is_category_model = issubclass(model, Category)

        async for obj in model.find_all(fetch_links=True, nesting_depth=1):
            if is_category_model:
                model_instance = CategoryResponse.model_validate(obj)
            else:
                model_instance = EventResponse.model_validate(obj)
            res.append(model_instance.dict(exclude_none=True))

        return res

    async def get_categories_dict(self) -> dict:
        categories_dict = {}
        categories = await self.get_all(Category)
        for category in categories:
            categories_dict[category["id"]] = category["name"]
        return categories_dict

    async def delete_one(self, model, criteria) -> dict:
        obj = await model.find_one(criteria)
        if obj:
            await obj.delete()
            return {"status": "deleted"}
        else:
            return {"error": "not found"}

    async def update(self, model: Document, criteria, update_data: EventUpdate, img=None, obj_id: str = None) -> dict:
        print(update_data)
        if update_data.category is not None:
            category_validation = await validate_id(update_data.category)
            if not category_validation.get("is_valid"):
                return category_validation

            category = category_validation.get("category")
            update_data.category = DBRef("category", category.id)

        update_dict = update_data.model_dump(exclude_none=True)

        if not update_dict:
            return {"message": "No changes provided."}

        if img:
            obj = await self.get_one(model, model.id == ObjectId(obj_id))
            model_name = model.get_settings().name
            directory_path = os.path.join("images", model_name)
            save_path = os.path.join(directory_path, f"{obj.get('id')}")
            with open(save_path, "wb") as new_file:
                shutil.copyfileobj(img.file, new_file)
            with Image.open(save_path) as img:
                img = img.resize((350, 350))
                new_save_path = os.path.splitext(save_path)[0] + ".webp"
                img.save(new_save_path, "WEBP")
            update_dict["img_path"] = os.path.relpath(new_save_path, start="images")

        update_result = await model.find(criteria).update({"$set": update_dict})

        if update_result.modified_count == 0 and not img:
            return {"message": "No changes made or object not found."}
        response = {
                "message": "Object updated successfully.", "id": str(criteria["_id"])
            }
        if img:
            response["new_save_path"] = new_save_path
            return response
        else:
            return response
