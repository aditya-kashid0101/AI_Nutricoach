from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    age: int = Field(ge=13, le=100)
    gender: str
    height_cm: float = Field(gt=100, le=250)
    weight_kg: float = Field(gt=30, le=300)
    fitness_goal: str
    activity_level: str


class ProfileResponse(ProfileRequest):
    id: int
    user_id: int

    model_config = {"from_attributes": True}
