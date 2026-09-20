from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    meal: str = "next meal"
    preferences: str = Field(default="", max_length=1000)


class RecommendationResponse(BaseModel):
    source: str
    recommendation: str
