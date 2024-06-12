from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from database.database import get_db
from schemas.recipe import UpdateRecipe, DeleteRecipe
from CRUD.recipe import update_recipe as update_recipe_crud, delete_recipe as delete_recipe_crud

router = APIRouter()

@router.put("/recipe/{recipe_id}", response_model=UpdateRecipe)
async def update_recipe(recipe_id: str, update_recipe: UpdateRecipe, db: AsyncIOMotorCollection = Depends(get_db)):
    updated_recipe = await update_recipe_crud(recipe_id, update_recipe.model_dump(), db)
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/recipe/{recipe_id}", response_model=DeleteRecipe)
async def delete_recipe(recipe_id: str, db: AsyncIOMotorCollection = Depends(get_db)):
    deleted_recipe = await delete_recipe_crud(recipe_id, db)
    if not deleted_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return deleted_recipe


# router.post("/recipe/{recipe_id}", response_model= recipe.UpdateRecipe)