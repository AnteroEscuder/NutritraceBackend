from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.models.meal import Meal
from app.models.food import Food
from sqlalchemy import Date

from app.utils.security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()



@router.put("/{user_id}", response_model=UserOut)
@router.patch("/{user_id}", response_model=UserOut)
def upate_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Solo puede modificar el propio usuario
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if payload.email:
        exists = db.query(User).filter(User.email == payload.email, User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="El email ya está en uso")
        user.email = payload.email

    if payload.name:
        user.name = payload.name

    if payload.password:
        user.password_hash = hash_password(payload.password)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    # TODO Devolver un json con una info de funciona
    return


def ensure_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta operación",
        )


@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_admin(current_user)
    users = db.query(User).all()
    return users


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}/summary")
def get_daily_summary(
    user_id: int,
    date_param: date = Query(..., alias="date"),
    db: Session = Depends(get_db)
):
    # Buscar comidas del usuario en esa fecha
    meals = (
        db.query(Meal)
        .filter(Meal.user_id == user_id)
        .filter(Meal.date.cast(Date) == date_param)
        .all()
    )

    if not meals:
        return {
            "date": date_param,
            "user_id": user_id,
            "total_calories": 0,
            "total_protein": 0,
            "total_carbs": 0,
            "total_fat": 0,
            "meals": []
        }

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    meal_details = []

    for meal in meals:
        food = meal.food
        q = meal.quantity / 100  # los datos nutricionales son por 100g

        total_calories += food.calories * q
        total_protein += food.protein * q
        total_carbs += food.carbs * q
        total_fat += food.fat * q

        meal_details.append({
            "food": food.name,
            "quantity": meal.quantity,
            "calories": food.calories * q
        })

    return {
        "date": date_param,
        "user_id": user_id,
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "total_carbs": round(total_carbs, 2),
        "total_fat": round(total_fat, 2),
        "meals": meal_details
    }

@router.get("/{user_id}/summary2")
def get_daily_summary2(
    user_id: int,
    date_param: date = Query(..., alias="date"),
    db: Session = Depends(get_db)
):
    meals = (
        db.query(Meal)
        .filter(Meal.user_id == user_id)
        .filter(Meal.date.cast(Date) == date_param)
        .all()
    )

    if not meals:
        return {
            "date": date_param,
            "user_id": user_id,
            "total_calories": 0,
            "total_protein": 0,
            "total_carbs": 0,
            "total_fat": 0,
            "meals": [],
            "message": "No se han registrado comidas ese día"
        }

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    meal_details = []

    for meal in meals:
        food = meal.food
        q = meal.quantity / 100 

        total_calories += food.calories * q
        total_protein += food.protein * q
        total_carbs += food.carbs * q
        total_fat += food.fat * q

        meal_details.append({
            "food": food.name,
            "quantity": meal.quantity,
            "calories": round(food.calories * q, 2)
        })

    # Intentar obtener los objetivos del usuario
    goal = db.query(Goal).filter(Goal.user_id == user_id).first()

    response = {
        "date": date_param,
        "user_id": user_id,
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "total_carbs": round(total_carbs, 2),
        "total_fat": round(total_fat, 2),
        "meals": meal_details
    }

    if goal:
        response.update({
            "target_calories": goal.calories,
            "target_protein": goal.protein,
            "target_carbs": goal.carbs,
            "target_fat": goal.fat,
            "status": {
                "calories": "✅" if total_calories <= goal.calories else "❌",
                "protein": "✅" if total_protein >= goal.protein else "❌",
                "carbs": "✅" if total_carbs <= goal.carbs else "❌",
                "fat": "✅" if total_fat <= goal.fat else "❌"
            }
        })

    return response