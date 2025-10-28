from pydantic import BaseModel
from datetime import date

class MealBase(BaseModel):
    user_id: int
    food_id: int
    quantity: float

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    food_id: int
    quantity: float
    date: date

class MealOut(MealBase):
    id: int
    user_id: int
    food_id: int
    quantity: float
    calories: float
    protein: float
    carbs: float
    fat: float
    food_name: str

    class Config:
        orm_mode = True

class MealSummary(BaseModel):
    date: date
    calories: float
    protein: float
    carbs: float
    fat: float
