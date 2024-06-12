from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class UpdateRecipe(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None

class DeleteRecipe(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
