import asyncio

from google import genai

from app.core.config import settings


SYSTEM_PROMPT = """
You are NutriCoach, a practical AI nutrition recommendation assistant.

Use the deterministic nutrition targets supplied by the backend as facts.
Do not recalculate BMR, TDEE, calories, or macros yourself.

The user context contains daily targets, logged intake, and remaining
calories/macros. Use those values when deciding what kind of meal to suggest.

Give a practical recommendation for the requested meal. Prefer familiar,
realistic foods and simple combinations. The recommendation should fit the
remaining nutrition budget as closely as practical.

Do not claim exact calories or exact macros for homemade meals unless the
backend has supplied those values. Do not provide medical diagnosis.

Keep the response concise and useful. Mention why the suggested meal fits
the user's remaining targets.
"""


async def generate_ai_recommendation(
    user_context: str,
    meal: str,
    preferences: str,
) -> tuple[str, str]:
    api_key = getattr(settings, "gemini_api_key", None)

    if not api_key:
        return (
            "fallback",
            "AI provider is not configured yet. Add GEMINI_API_KEY to "
            "backend/.env to enable generated recommendations.",
        )

    model = getattr(settings, "gemini_model", "gemini-3.6-flash")

    user_prompt = (
        f"User context: {user_context}\n"
        f"Requested meal: {meal}\n"
        f"Preferences: {preferences or 'none provided'}"
    )

    try:
        client = genai.Client(api_key=api_key)

        interaction = await asyncio.to_thread(
            client.interactions.create,
            model=model,
            input=f"{SYSTEM_PROMPT}\n\n{user_prompt}",
        )

        text = (interaction.output_text or "").strip()

        if not text:
            raise RuntimeError("Gemini returned an empty response")

        return "ai", text

    except Exception as exc:
        print(f"Gemini recommendation error: {exc}")
        return (
            "fallback",
            "The AI provider could not be reached, so NutriCoach returned "
            "a fallback recommendation. Check GEMINI_API_KEY and GEMINI_MODEL "
            "in backend/.env.",
        )
