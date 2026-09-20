from pydantic import BaseModel, Field


class NutritionResponse(BaseModel):
    bmr: float
    tdee: float
    activity_multiplier: float
    calorie_target: float
    protein_g: float
    carbs_g: float
    fat_g: float
    goal: str
    explanation: str


class FoodResponse(BaseModel):
    id: int
    name: str
    category: str
    calories: float
    protein: float
    carbs: float
    fat: float
    serving_g: float
    vegetarian: bool

    model_config = {"from_attributes": True}


class IntakeCreate(BaseModel):
    food_id: int
    servings: float = Field(gt=0, le=20)
    meal_type: str = "meal"


class IntakeResponse(BaseModel):
    id: int
    food_id: int
    food_name: str
    servings: float
    meal_type: str
    calories: float
    protein: float
    carbs: float
    fat: float
