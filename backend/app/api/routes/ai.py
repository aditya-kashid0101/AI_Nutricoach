from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import generate_ai_response


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Coach"],
)


@router.post("/chat", response_model=AIChatResponse)
def chat_with_ai(
    request: AIChatRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        response = generate_ai_response(request.message)

        return AIChatResponse(
            response=response,
        )

    except Exception as exc:
        print(f"AI ERROR: {exc}")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc