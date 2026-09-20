from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, UserProfile
from app.schemas.profile import ProfileRequest, ProfileResponse

router = APIRouter()


@router.get("", response_model=ProfileResponse | None)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserProfile).filter(UserProfile.user_id == user.id).first()


@router.put("", response_model=ProfileResponse)
def upsert_profile(
    payload: ProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)

    for key, value in payload.model_dump().items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
