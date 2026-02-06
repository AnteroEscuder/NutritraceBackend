from app.database import SessionLocal
from app.models.allergen import Allergen

DEFAULT = [
    "Gluten", "Lactosa", "Huevo", "Cacahuete", "Frutos secos", "Soja",
    "Pescado", "Marisco", "Sésamo", "Mostaza", "Apio", "Sulfitos"
]

db = SessionLocal()
for name in DEFAULT:
    exists = db.query(Allergen).filter(Allergen.name == name).first()
    if not exists:
        db.add(Allergen(name=name))
db.commit()
db.close()
print("✅ Alérgenos insertados")
