from pydantic import BaseModel

class GoalBase(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    user_id: int

    class Config:
        orm_mode = True
