from google import genai

from app.core.config import settings


if not settings.gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(
    api_key=settings.gemini_api_key,
)


SYSTEM_PROMPT = """
You are NutriCoach, a helpful AI nutrition and fitness assistant.

Your job is to:
- answer nutrition and fitness questions clearly
- provide practical meal and nutrition suggestions
- explain recommendations simply
- consider user information when it is provided
- never invent user information

Important:
- Do not claim your calculations are medically authoritative.
- Do not invent exact calories or nutrition values when reliable data has not been provided.
- The NutriCoach backend will provide authoritative nutrition calculations.
- For now, focus on conversational nutrition guidance.
"""


def generate_ai_response(message: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

User:
{message}
"""

    interaction = client.interactions.create(
        model=settings.gemini_model,
        input=prompt,
    )

    return interaction.output_text