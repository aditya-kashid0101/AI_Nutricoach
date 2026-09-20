from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.nutrition import NutritionResponse
from app.services.nutrition import calculate_nutrition

router = APIRouter()


@router.get("/summary", response_model=NutritionResponse)
def nutrition_summary(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.profile:
        raise HTTPException(
            status_code=400,
            detail="Complete your profile first",
        )

    p = user.profile

    try:
        result = calculate_nutrition(
            p.age,
            p.gender,
            p.height_cm,
            p.weight_kg,
            p.activity_level,
            p.fitness_goal,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    db.execute(
        text(
            """
            INSERT INTO nutrition_history (
                user_id,
                age,
                gender,
                height_cm,
                weight_kg,
                activity_level,
                goal,
                bmr,
                tdee,
                activity_multiplier,
                calorie_target,
                protein_g,
                carbs_g,
                fat_g
            )
            VALUES (
                :user_id,
                :age,
                :gender,
                :height_cm,
                :weight_kg,
                :activity_level,
                :goal,
                :bmr,
                :tdee,
                :activity_multiplier,
                :calorie_target,
                :protein_g,
                :carbs_g,
                :fat_g
            )
            """
        ),
        {
            "user_id": user.id,
            "age": p.age,
            "gender": p.gender,
            "height_cm": p.height_cm,
            "weight_kg": p.weight_kg,
            "activity_level": p.activity_level,
            "goal": p.fitness_goal,
            "bmr": result["bmr"],
            "tdee": result["tdee"],
            "activity_multiplier": result["activity_multiplier"],
            "calorie_target": result["calorie_target"],
            "protein_g": result["protein_g"],
            "carbs_g": result["carbs_g"],
            "fat_g": result["fat_g"],
        },
    )
    db.commit()

    return result
