from app.database import Base, engine
from app.models.user import User
from app.models.food import Food
from app.models.meal import Meal
from app.models.user import User
from app.models.food import Food
from app.models.meal import Meal
from app.models.goal import Goal

print("📦 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente")

Base.metadata.drop_all(bind=engine)  # ⚠️ Borra todo
Base.metadata.create_all(bind=engine)
