from typing import Any, Dict
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

async def update_recipe(recipe_id: str, update_data: Dict[str, Any], db: AsyncIOMotorCollection) -> object:
    recipe_data = {k: v for k, v in update_data.items() if v is not None}
    result = await db.update_one({"_id": ObjectId(recipe_id)}, {"$set": recipe_data})

    if result.matched_count == 0:
        return None

    updated_recipe = await db.find_one({"_id": ObjectId(recipe_id)})
    return updated_recipe

async def delete_recipe(recipe_id: str, db: AsyncIOMotorCollection) -> object:
    result = await db.delete_one({"_id": ObjectId(recipe_id)})

    if result.deleted_count == 0:
        return None

    return {"_id": recipe_id}
