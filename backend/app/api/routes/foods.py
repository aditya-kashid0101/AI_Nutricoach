from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.food import Food
from app.models.nutrition import FoodIntake
from app.models.user import User
from app.schemas.nutrition import FoodResponse, IntakeCreate, IntakeResponse

router = APIRouter()


@router.get("", response_model=list[FoodResponse])
def list_foods(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Food).order_by(Food.name).all()


@router.post("/intake", response_model=IntakeResponse, status_code=201)
def log_intake(
    payload: IntakeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    food = db.get(Food, payload.food_id)
    if not food:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Food not found")

    log = FoodIntake(
        user_id=user.id,
        food_id=food.id,
        servings=payload.servings,
        meal_type=payload.meal_type,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return IntakeResponse(
        id=log.id,
        food_id=food.id,
        food_name=food.name,
        servings=log.servings,
        meal_type=log.meal_type,
        calories=round(food.calories * log.servings, 1),
        protein=round(food.protein * log.servings, 1),
        carbs=round(food.carbs * log.servings, 1),
        fat=round(food.fat * log.servings, 1),
    )


@router.get("/intake", response_model=list[IntakeResponse])
def list_intake(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    logs = (
        db.query(FoodIntake)
        .filter(FoodIntake.user_id == user.id)
        .order_by(FoodIntake.logged_at.desc())
        .limit(30)
        .all()
    )
    return [
        IntakeResponse(
            id=x.id,
            food_id=x.food_id,
            food_name=x.food.name,
            servings=x.servings,
            meal_type=x.meal_type,
            calories=round(x.food.calories * x.servings, 1),
            protein=round(x.food.protein * x.servings, 1),
            carbs=round(x.food.carbs * x.servings, 1),
            fat=round(x.food.fat * x.servings, 1),
        )
        for x in logs
    ]
