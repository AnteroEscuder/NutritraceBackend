from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class FoodAllergen(Base):
    __tablename__ = "food_allergens"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.id"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint("food_id", "allergen_id", name="uq_food_allergen"),)
