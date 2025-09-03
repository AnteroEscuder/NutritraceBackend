from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.meal import Meal
from app.models.user import User
from app.models.food import Food
from app.schemas.meal import MealCreate, MealOut, MealSummary
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/meals", tags=["Meals"])

# @router.get("/", response_model=list[MealOut])
# def list_meals(db: Session = Depends(get_db)):
#     meals = db.query(Meal).all()
#     result = []

#     for meal in meals:
#         result.append(factorConversion(meal))

#     return result


@router.post("/", response_model=MealOut)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    # Verificar que usuario existe
    user = db.query(User).filter(User.id == meal.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que alimento existe
    food = db.query(Food).filter(Food.id == meal.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    db_meal = Meal(
        user_id=meal.user_id,
        food_id=meal.food_id,
        quantity=meal.quantity
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return factorConversion(meal, food, db_meal)

# TODO Proteger rutas
@router.get("/summary/{user_id}", response_model=list[MealSummary])
def get_meal_summary(user_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            Meal.date,
            func.sum(Food.calories * (Meal.quantity / 100)).label("calories"),
            func.sum(Food.protein * (Meal.quantity / 100)).label("protein"),
            func.sum(Food.carbs * (Meal.quantity / 100)).label("carbs"),
            func.sum(Food.fat * (Meal.quantity / 100)).label("fat"),
        )
        .join(Food, Meal.food_id == Food.id)
        .filter(Meal.user_id == user_id)
        .group_by(Meal.date)
        .order_by(Meal.date.desc())
        .all()
    )

    return [
        {
            "date": r.date,
            "calories": r.calories,
            "protein":  r.protein,
            "carbs":  r.carbs,
            "fat":  r.fat
        } for r in results
    ]

@router.get("/", response_model=List[MealOut])
def get_meals(
    user_id: int = Query(None),
    date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Meal)
    if user_id:
        query = query.filter(Meal.user_id == user_id)
    if date:
        query = query.filter(Meal.date == date)
    
    meals = query.all()
    return [factorConversion(meal, food=meal.food) for meal in meals]


def factorConversion(meal, food=None, db_meal=None):

    if food is None:
        food = meal.food

    factor = meal.quantity / 100 # Calcular valores nutricionales

    return {
        "id": db_meal.id if db_meal else meal.id,
        "user_id": db_meal.user_id if db_meal else meal.user_id,
        "food_id":  db_meal.food_id if db_meal else meal.food_id,
        "quantity": db_meal.quantity if db_meal else meal.quantity,
        "calories": food.calories * factor,
        "protein": food.protein * factor,
        "carbs": food.carbs * factor,
        "fat": food.fat * factor,
        "food_name": food.name
    }