from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.food import Food
from app.models.meal import Meal
from app.schemas.meal import MealCreate, MealOut, MealUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/meals", tags=["Meals"])


def get_accessible_food(db: Session, food_id: int, current_user: User):
    return db.query(Food).filter(
        Food.id == food_id,
        or_(
            Food.is_system.is_(True),
            Food.user_id == current_user.id,
        ),
    ).first()


@router.post("/", response_model=MealOut, status_code=status.HTTP_201_CREATED)
def create_meal(
    meal: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    food = get_accessible_food(db, meal.food_id, current_user)
    if not food:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    db_meal = Meal(
        user_id=current_user.id,
        food_id=meal.food_id,
        quantity=meal.quantity,
        date=meal.date or date.today(),
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    factor = (db_meal.quantity or 0) / 100.0

    return {
        "id": db_meal.id,
        "user_id": db_meal.user_id,
        "food_id": db_meal.food_id,
        "quantity": db_meal.quantity,
        "date": db_meal.date,
        "food_name": food.name,
        "calories": (food.calories or 0) * factor,
        "protein": (food.protein or 0) * factor,
        "carbs": (food.carbs or 0) * factor,
        "fat": (food.fat or 0) * factor,
    }

@router.get("/", response_model=List[MealOut])
def list_meals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    day: Optional[date] = Query(None, description="Filtrar por fecha"),
):
    q = db.query(Meal, Food).join(Food, Food.id == Meal.food_id).filter(Meal.user_id == current_user.id)

    if day:
        q = q.filter(Meal.date == day)

    rows = q.all()

    out = []
    for meal, food in rows:
        factor = (meal.quantity or 0) / 100.0
        out.append({
            "id": meal.id,
            "user_id": meal.user_id,
            "food_id": meal.food_id,
            "quantity": meal.quantity,
            "date": meal.date,
            "food_name": food.name,
            "calories": (food.calories or 0) * factor,
            "protein": (food.protein or 0) * factor,
            "carbs": (food.carbs or 0) * factor,
            "fat": (food.fat or 0) * factor,
        })

    return out


@router.put("/{meal_id}", response_model=MealOut)
def update_meal(
    meal_id: int,
    meal: MealUpdate,
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
        food = get_accessible_food(db, meal.food_id, current_user)
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

    # Obtener el alimento actualizado para nombre/macros
    food = get_accessible_food(db, db_meal.food_id, current_user)
    if not food:
        # no debería pasar, pero por seguridad
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    factor = (db_meal.quantity or 0) / 100.0

    return {
        "id": db_meal.id,
        "user_id": db_meal.user_id,
        "food_id": db_meal.food_id,
        "quantity": db_meal.quantity,
        "date": db_meal.date,
        "food_name": food.name,
        "calories": (food.calories or 0) * factor,
        "protein": (food.protein or 0) * factor,
        "carbs": (food.carbs or 0) * factor,
        "fat": (food.fat or 0) * factor,
    }


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
