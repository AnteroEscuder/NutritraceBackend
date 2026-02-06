from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.allergen import Allergen
from app.models.user_allergen import UserAllergen
from app.schemas.allergen import AllergenOut
from app.schemas.profile import UserAllergiesUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/allergies", response_model=list[AllergenOut])
def get_my_allergies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Allergen)
        .join(UserAllergen, UserAllergen.allergen_id == Allergen.id)
        .filter(UserAllergen.user_id == current_user.id)
        .order_by(Allergen.name.asc())
        .all()
    )
    return rows


@router.put("/allergies", response_model=list[AllergenOut])
def update_my_allergies(
    payload: UserAllergiesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.query(UserAllergen).filter(UserAllergen.user_id == current_user.id).delete()

    for aid in payload.allergen_ids:
        db.add(UserAllergen(user_id=current_user.id, allergen_id=aid))

    db.commit()

    rows = (
        db.query(Allergen)
        .join(UserAllergen, UserAllergen.allergen_id == Allergen.id)
        .filter(UserAllergen.user_id == current_user.id)
        .order_by(Allergen.name.asc())
        .all()
    )
    return rows
