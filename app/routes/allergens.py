from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.allergen import Allergen
from app.schemas.allergen import AllergenOut

router = APIRouter(prefix="/allergens", tags=["Allergens"])

@router.get("/", response_model=list[AllergenOut])
def list_allergens(db: Session = Depends(get_db)):
    return db.query(Allergen).order_by(Allergen.name.asc()).all()
