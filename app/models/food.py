from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 👈 quito unique=True, el nombre se repite entre usuarios
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)

    # 🔹 Dueño del alimento
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="foods")
