from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.food import Food
from app.schemas.food import FoodCreate, FoodOut
from app.utils.security import get_current_user

router = APIRouter(prefix="/foods", tags=["Foods"])


@router.get("/", response_model=List[FoodOut])
def list_foods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: Optional[str] = Query(None, description="Buscar por nombre"),
):
    """
    Lista los alimentos del USUARIO ACTUAL.
    Cada usuario solo ve los suyos.
    """
    query = db.query(Food).filter(Food.user_id == current_user.id)

    if search:
        query = query.filter(Food.name.ilike(f"%{search}%"))

    return query.all()


@router.get("/{food_id}", response_model=FoodOut)
def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve un alimento del usuario actual.
    """
    food = (
        db.query(Food)
        .filter(Food.id == food_id, Food.user_id == current_user.id)
        .first()
    )
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado",
        )
    return food


@router.post("/", response_model=FoodOut, status_code=status.HTTP_201_CREATED)
def create_food(
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea un alimento para el usuario actual.
    El mismo nombre se puede repetir entre distintos usuarios.
    """
    # Opcional: impedir nombre duplicado para ESTE usuario
    existing = (
        db.query(Food)
        .filter(Food.user_id == current_user.id, Food.name == food.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tienes un alimento con ese nombre",
        )

    db_food = Food(
        name=food.name,
        calories=food.calories,
        protein=food.protein,
        carbs=food.carbs,
        fat=food.fat,
        user_id=current_user.id,
    )
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@router.put("/{food_id}", response_model=FoodOut)
def update_food(
    food_id: int,
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza un alimento del usuario.
    No puedes editar alimentos de otro usuario.
    """
    db_food = (
        db.query(Food)
        .filter(Food.id == food_id, Food.user_id == current_user.id)
        .first()
    )
    if not db_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado",
        )

    # Comprobar que el nuevo nombre no choque con otro alimento del mismo usuario
    if food.name != db_food.name:
        name_in_use = (
            db.query(Food)
            .filter(Food.user_id == current_user.id, Food.name == food.name)
            .first()
        )
        if name_in_use:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes otro alimento con ese nombre",
            )

    db_food.name = food.name
    db_food.calories = food.calories
    db_food.protein = food.protein
    db_food.carbs = food.carbs
    db_food.fat = food.fat

    db.commit()
    db.refresh(db_food)
    return db_food


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Borra un alimento del usuario.
    No puedes borrar alimentos de otro.
    """
    db_food = (
        db.query(Food)
        .filter(Food.id == food_id, Food.user_id == current_user.id)
        .first()
    )
    if not db_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado",
        )

    db.delete(db_food)
    db.commit()
    return None
