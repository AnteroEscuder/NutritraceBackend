from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.allergen import Allergen
from app.models.user_allergen import UserAllergen
from app.schemas.allergen import AllergenOut
from app.schemas.profile import UserAllergiesUpdate
from app.utils.security import get_current_user
import os
from uuid import uuid4
from fastapi import UploadFile, File, HTTPException
from app.schemas.user import UserOut, UserProfileUpdate

UPLOAD_DIR = "static/profile_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@router.post("/photo", response_model=UserOut)
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Formato no permitido")

    old_url = current_user.profile_image_url

    ext = file.filename.split(".")[-1].lower()
    filename = f"user_{current_user.id}_{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    if old_url:
        old_path = old_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    current_user.profile_image_url = f"/static/profile_photos/{filename}"

    db.commit()
    db.refresh(current_user)

    return current_user

@router.put("/me", response_model=UserOut)
def update_my_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(User)
        .filter(User.email == payload.email, User.id != current_user.id)
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Ese email ya está en uso")

    current_user.name = payload.name
    current_user.email = payload.email

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/photo", response_model=UserOut)
def delete_profile_photo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_url = current_user.profile_image_url

    if old_url:
        old_path = old_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    current_user.profile_image_url = None

    db.commit()
    db.refresh(current_user)

    return current_user