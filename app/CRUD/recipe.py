from typing import Any, Collection, Dict
from bson import ObjectId
import os
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException, UploadFile
import uuid
from utils.img import resize_image

async def update_recipe(recipe_id: str, update_data: Dict[str, Any], db: AsyncIOMotorCollection) -> object:
    recipe_data = {key: value for key, value in update_data.items() if value is not None}
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


async def upload_image(recipe_id: str, file: UploadFile, collection):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File is not an image")

    resized_image = await resize_image(file)

    # Unique name for image like user ID
    filename = f"{uuid.uuid4()}.jpg"

    import os
    os.makedirs("images", exist_ok=True)

    with open(f"images/{filename}", "wb") as f:
        f.write(resized_image.getvalue())

    await collection.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$set": {"image_path": filename}}
    )

    return JSONResponse(status_code=200, content={"message": "Image uploaded successfully", "filename": filename})
