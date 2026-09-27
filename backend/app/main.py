import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai
from app.api.routes import auth, foods, nutrition, profile, recommendation
from app.db.base import Base
from app.db.session import engine
from app.models import Food, FoodIntake, Recommendation, User, UserProfile
from app.services.seed import seed_foods


Base.metadata.create_all(bind=engine)
seed_foods()

app = FastAPI(title="NutriCoach API", version="1.0.0")

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
configured_origins = os.getenv("FRONTEND_ORIGINS", "")
frontend_origins = [
    origin.strip()
    for origin in configured_origins.split(",")
    if origin.strip()
]
allowed_origins = list(dict.fromkeys(default_origins + frontend_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(foods.router, prefix="/api/foods", tags=["Food"])
app.include_router(
    recommendation.router,
    prefix="/api/recommendations",
    tags=["AI Recommendations"],
)
app.include_router(ai.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NutriCoach API"}
