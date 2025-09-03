from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Date, func

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Float, nullable=False)  # gramos
    date = Column(Date, server_default=func.current_date())

    # Relaciones
    user = relationship("User", backref="meals")
    food = relationship("Food", backref="meals", lazy="joined")
