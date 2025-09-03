from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.food import Food
from app.models.user import User
from app.schemas.food import FoodCreate, FoodOut
from app.utils.security import get_current_user

router = APIRouter(prefix="/foods", tags=["Foods"])

@router.post("/", response_model=FoodOut)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    existing_food = db.query(Food).filter(Food.name == food.name).first()
    if existing_food:
        raise HTTPException(status_code=400, detail="El alimento ya existe")

    db_food = Food(
        name=food.name,
        calories=food.calories,
        protein=food.protein,
        carbs=food.carbs,
        fat=food.fat
    )
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@router.get("/", response_model=List[FoodOut])
def search_foods(name: str = Query(None),db: Session = Depends(get_db)):
    if name:
        return db.query(Food).filter(Food.name.ilike(f"%{name}%")).all()
    return db.query(Food).all()

@router.put("/{id}", response_model=FoodOut)
def update_food(id: int, food: FoodCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_food = db.query(Food).filter(Food.id == id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    db_food.name = food.name
    db_food.calories = food.calories
    db_food.protein = food.protein
    db_food.carbs = food.carbs
    db_food.fat = food.fat

    db.commit()
    db.refresh(db_food)
    return db_food

# TODO Problema al borrar la food porque esta relacionada con meal
@router.delete("/{id}", response_model=FoodOut)
def update_food(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_food = db.query(Food).filter(Food.id == id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    if db_food.meals:
        raise HTTPException(status_code=400, detail="El alimento está en uso y no se puede eliminar")

    db.delete(db_food)
    db.commit()
    return db_food