from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalOut
from app.utils.security import get_current_user

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=GoalOut)
def get_my_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes objetivos configurados todavía",
        )
    return goal


@router.post("/", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_or_update_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_goal = db.query(Goal).filter(Goal.user_id == current_user.id).first()

    if db_goal:
        # Actualizar
        db_goal.calories = goal.calories
        db_goal.protein = goal.protein
        db_goal.carbs = goal.carbs
        db_goal.fat = goal.fat
    else:
        # Crear
        db_goal = Goal(
            user_id=current_user.id,
            calories=goal.calories,
            protein=goal.protein,
            carbs=goal.carbs,
            fat=goal.fat,
        )
        db.add(db_goal)

    db.commit()
    db.refresh(db_goal)
    return db_goal
