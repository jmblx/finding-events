from bson import ObjectId
from bson.errors import InvalidId

from event.models import Category


async def validate_id(cat_id: str):
    try:
        if not await Category.find_one(Category.id == ObjectId(cat_id)):
            return {"is_valid": False, "error": "category not found"}
        else:
            return {"is_valid": True}
    except InvalidId:
        return {"is_valid": False, "error": "category_id incorrect format"}