from pydantic import BaseModel
from typing import List
from app.schemas.allergen import AllergenOut

class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    allergen_ids: List[int] = []

class FoodCreate(FoodBase):
    pass

class FoodOut(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    allergens: List[AllergenOut] = []

    class Config:
        from_attributes = True