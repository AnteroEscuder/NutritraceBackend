from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.goal import Goal
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalOut

router = APIRouter(prefix="/goals", tags=["Goals"])

@router.post("/{user_id}", response_model=GoalOut)
def set_goal(user_id: int, goal: GoalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existing = db.query(Goal).filter(Goal.user_id == user_id).first()
    if existing:
        existing.calories = goal.calories
        existing.protein = goal.protein
        existing.carbs = goal.carbs
        existing.fat = goal.fat
    else:
        new_goal = Goal(user_id=user_id, **goal.dict())
        db.add(new_goal)

    db.commit()
    return db.query(Goal).filter(Goal.user_id == user_id).first()

@router.get("/{user_id}", response_model=GoalOut)
def get_goal(user_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Objetivo no establecido")
    return goal
