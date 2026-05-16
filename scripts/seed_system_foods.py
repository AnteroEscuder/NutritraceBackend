from app.database import SessionLocal
from app.models.food import Food
from app.models.user import User  # noqa: F401


DEFAULT_SYSTEM_FOODS = [
    {"name": "Arroz blanco cocido", "calories": 130.0, "protein": 2.7, "carbs": 28.0, "fat": 0.3},
    {"name": "Pechuga de pollo", "calories": 165.0, "protein": 31.0, "carbs": 0.0, "fat": 3.6},
    {"name": "Avena", "calories": 389.0, "protein": 16.9, "carbs": 66.3, "fat": 6.9},
    {"name": "Huevo", "calories": 155.0, "protein": 13.0, "carbs": 1.1, "fat": 11.0},
    {"name": "Manzana", "calories": 52.0, "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    {"name": "Platano", "calories": 89.0, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
    {"name": "Yogur natural", "calories": 61.0, "protein": 3.5, "carbs": 4.7, "fat": 3.3},
    {"name": "Aceite de oliva", "calories": 884.0, "protein": 0.0, "carbs": 0.0, "fat": 100.0},
    {"name": "Pan integral", "calories": 247.0, "protein": 13.0, "carbs": 41.0, "fat": 4.2},
    {"name": "Lentejas cocidas", "calories": 116.0, "protein": 9.0, "carbs": 20.0, "fat": 0.4},
]


def main():
    db = SessionLocal()
    try:
        created = 0
        for data in DEFAULT_SYSTEM_FOODS:
            exists = (
                db.query(Food)
                .filter(Food.name == data["name"], Food.is_system.is_(True))
                .first()
            )
            if exists:
                continue

            db.add(Food(**data, user_id=None, is_system=True))
            created += 1

        db.commit()
        print(f"System foods inserted: {created}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
