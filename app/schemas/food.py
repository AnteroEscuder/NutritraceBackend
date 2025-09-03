from pydantic import BaseModel

class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class FoodCreate(FoodBase):
    pass

class FoodOut(FoodBase):
    id: int

    class Config:
        orm_model = True