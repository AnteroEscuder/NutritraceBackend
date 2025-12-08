from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.food import Food
from app.models.meal import Meal
from app.schemas.meal import MealCreate, MealOut
from app.utils.security import get_current_user

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.post("/", response_model=MealOut, status_code=status.HTTP_201_CREATED)
def create_meal(
    meal: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verificar que el alimento existe
    food = db.query(Food).filter(Food.id == meal.food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado",
        )

    db_meal = Meal(
        user_id=current_user.id,
        food_id=meal.food_id,
        quantity=meal.quantity,
        date=meal.date or date.today(),
    )

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.get("/", response_model=List[MealOut])
def list_meals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    day: Optional[date] = Query(None, description="Filtrar por fecha"),
):
    query = db.query(Meal).filter(Meal.user_id == current_user.id)
    if day:
        query = query.filter(Meal.date == day)
    return query.all()


@router.put("/{meal_id}", response_model=MealOut)
def update_meal(
    meal_id: int,
    meal: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_meal = db.query(Meal).filter(
        Meal.id == meal_id, Meal.user_id == current_user.id
    ).first()
    if not db_meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de comida no encontrado",
        )

    # Si se cambia el alimento, comprobar que existe
    if meal.food_id != db_meal.food_id:
        food = db.query(Food).filter(Food.id == meal.food_id).first()
        if not food:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado",
            )

    db_meal.food_id = meal.food_id
    db_meal.quantity = meal.quantity
    db_meal.date = meal.date or db_meal.date

    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_meal = db.query(Meal).filter(
        Meal.id == meal_id, Meal.user_id == current_user.id
    ).first()
    if not db_meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de comida no encontrado",
        )

    db.delete(db_meal)
    db.commit()
    return None
