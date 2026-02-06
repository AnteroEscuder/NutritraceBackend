from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class UserAllergen(Base):
    __tablename__ = "user_allergens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.id"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint("user_id", "allergen_id", name="uq_user_allergen"),)
