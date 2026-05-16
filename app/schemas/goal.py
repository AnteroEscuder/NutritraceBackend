from pydantic import BaseModel, ConfigDict

class GoalBase(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
