from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.nutrition import Recommendation
from app.models.user import User
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.ai import generate_ai_recommendation
from app.services.recommendation import build_user_context

router = APIRouter()


@router.post("", response_model=RecommendationResponse)
async def recommend(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user.profile:
        raise HTTPException(status_code=400, detail="Complete your profile first")

    context = build_user_context(db, user)
    source, text = await generate_ai_recommendation(
        context, payload.meal, payload.preferences
    )

    record = Recommendation(
        user_id=user.id,
        source=source,
        prompt=f"meal={payload.meal}; preferences={payload.preferences}",
        recommendation=text,
    )
    db.add(record)
    db.commit()

    return RecommendationResponse(source=source, recommendation=text)


@router.get("/history", response_model=list[RecommendationResponse])
def history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .limit(10)
        .all()
    )
    return [
        RecommendationResponse(source=x.source, recommendation=x.recommendation)
        for x in rows
    ]
