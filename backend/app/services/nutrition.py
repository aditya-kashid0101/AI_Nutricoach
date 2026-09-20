ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

SUPPORTED_GENDERS = {"male", "female"}
SUPPORTED_GOALS = {"weight_loss", "muscle_gain", "maintenance", "general_fitness"}


def calculate_nutrition(
    age: int,
    gender: str,
    height_cm: float,
    weight_kg: float,
    activity_level: str,
    goal: str,
) -> dict:
    """
    Deterministic nutrition calculation used by the existing Nutrition API.

    The function signature and returned dictionary are intentionally preserved
    so existing routes/frontend code do not need to be rewritten.
    """
    if not 13 <= age <= 100:
        raise ValueError("Age must be between 13 and 100.")

    if not 100 < height_cm <= 250:
        raise ValueError("Height must be between 100 and 250 cm.")

    if not 25 < weight_kg <= 300:
        raise ValueError("Weight must be between 25 and 300 kg.")

    gender_key = gender.strip().lower()
    if gender_key not in SUPPORTED_GENDERS:
        raise ValueError("Gender must be 'male' or 'female'.")

    activity_key = activity_level.strip().lower()
    if activity_key not in ACTIVITY_MULTIPLIERS:
        raise ValueError(
            "Activity level must be one of: sedentary, light, moderate, active, very_active."
        )

    goal_key = goal.strip().lower()
    if goal_key not in SUPPORTED_GOALS:
        raise ValueError(
            "Goal must be one of: weight_loss, muscle_gain, maintenance, general_fitness."
        )

    # Mifflin-St Jeor equation.
    if gender_key == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multiplier = ACTIVITY_MULTIPLIERS[activity_key]
    tdee = bmr * multiplier

    if goal_key == "weight_loss":
        calorie_target = tdee - 400
    elif goal_key == "muscle_gain":
        calorie_target = tdee + 250
    else:
        calorie_target = tdee

    calorie_target = max(calorie_target, 1200)

    # Goal-aware deterministic macro calculation.
    protein_per_kg = 1.8 if goal_key == "muscle_gain" else 1.6
    protein = weight_kg * protein_per_kg
    fat = weight_kg * 0.8
    remaining = max(calorie_target - protein * 4 - fat * 9, 0)
    carbs = remaining / 4

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "activity_multiplier": multiplier,
        "calorie_target": round(calorie_target),
        "protein_g": round(protein),
        "carbs_g": round(carbs),
        "fat_g": round(fat),
        "goal": goal_key,
        "explanation": (
            "BMR uses Mifflin-St Jeor, TDEE applies the selected activity "
            "multiplier, then the goal adjustment is applied. Macros are "
            "calculated deterministically from body weight and calorie target."
        ),
    }
