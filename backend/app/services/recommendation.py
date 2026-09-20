from sqlalchemy.orm import Session

from app.models.nutrition import FoodIntake
from app.models.user import User
from app.services.nutrition import calculate_nutrition


def build_user_context(db: Session, user: User) -> str:
    profile = user.profile
    if not profile:
        return "No nutrition profile has been completed."

    target = calculate_nutrition(
        profile.age,
        profile.gender,
        profile.height_cm,
        profile.weight_kg,
        profile.activity_level or "moderate",
        profile.fitness_goal or "maintenance",
    )

    intake = (
        db.query(FoodIntake)
        .filter(FoodIntake.user_id == user.id)
        .all()
    )

    calories = sum((x.food.calories or 0) * x.servings for x in intake)
    protein = sum((x.food.protein or 0) * x.servings for x in intake)
    carbs = sum((x.food.carbs or 0) * x.servings for x in intake)
    fat = sum((x.food.fat or 0) * x.servings for x in intake)

    remaining_calories = max(target["calorie_target"] - calories, 0)
    remaining_protein = max(target["protein_g"] - protein, 0)
    remaining_carbs = max(target["carbs_g"] - carbs, 0)
    remaining_fat = max(target["fat_g"] - fat, 0)

    return (
        f"Goal={profile.fitness_goal}; "
        f"Weight={profile.weight_kg} kg; "
        f"Daily calorie target={target['calorie_target']} kcal; "
        f"Protein target={target['protein_g']} g; "
        f"Carbohydrate target={target['carbs_g']} g; "
        f"Fat target={target['fat_g']} g; "
        f"Logged calories={round(calories)} kcal; "
        f"Logged protein={round(protein)} g; "
        f"Logged carbohydrates={round(carbs)} g; "
        f"Logged fat={round(fat)} g; "
        f"Remaining calories={round(remaining_calories)} kcal; "
        f"Remaining protein={round(remaining_protein)} g; "
        f"Remaining carbohydrates={round(remaining_carbs)} g; "
        f"Remaining fat={round(remaining_fat)} g."
    )
