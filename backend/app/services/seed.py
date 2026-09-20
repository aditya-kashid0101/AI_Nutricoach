from app.db.session import SessionLocal
from app.models.food import Food

FOODS = [
    ("Poha", "breakfast", 180, 4, 28, 6),
    ("Upma", "breakfast", 190, 5, 30, 6),
    ("Idli", "breakfast", 150, 5, 30, 1),
    ("Dosa", "breakfast", 170, 4, 28, 5),
    ("Roti", "meal", 120, 3.5, 22, 2),
    ("Cooked Rice", "meal", 130, 2.7, 28, 0.3),
    ("Dal", "meal", 120, 7, 18, 2),
    ("Rajma", "meal", 125, 8.5, 22, 0.5),
    ("Chole", "meal", 145, 7, 22, 4),
    ("Paneer", "protein", 265, 18, 6, 20),
    ("Curd", "snack", 61, 3.5, 4.7, 3.3),
    ("Banana", "snack", 89, 1.1, 23, 0.3),
    ("Apple", "snack", 52, 0.3, 14, 0.2),
    ("Egg", "protein", 155, 13, 1.1, 11),
    ("Chicken Breast", "protein", 165, 31, 0, 3.6),
    ("Mixed Sabzi", "vegetable", 80, 3, 12, 2),
]

def seed_foods():
    db = SessionLocal()
    try:
        if db.query(Food).count() == 0:
            for name, category, calories, protein, carbs, fat in FOODS:
                db.add(Food(
                    name=name,
                    category=category,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                    serving_g=100,
                    vegetarian=name not in {"Egg", "Chicken Breast"},
                ))
            db.commit()
    finally:
        db.close()
