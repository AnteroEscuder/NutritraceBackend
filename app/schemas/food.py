from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    allergens: List[AllergenOut] = []
