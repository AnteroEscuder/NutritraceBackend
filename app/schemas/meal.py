from pydantic import BaseModel, ConfigDict
import datetime as dt

class MealCreate(BaseModel):
    food_id: int
    quantity: float
    date: dt.date | None = None

class MealUpdate(BaseModel):
    food_id: int
    quantity: float
    date: dt.date | None = None

class MealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    food_id: int
    quantity: float
    calories: float
    protein: float
    carbs: float
    fat: float
    food_name: str
    date: dt.date
