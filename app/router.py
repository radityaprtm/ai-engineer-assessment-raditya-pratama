from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def classify_question(question: str):
    prompt = f"""
Classify the user's question into exactly one of these categories:

dataset
- Questions about space exploration, spacecraft, space missions,
  telescopes, Mars rovers, or the International Space Station.

superhero
- Questions about superheroes or villains.

both
- Questions that require information about both space exploration
  and superheroes or villains.

Question:
{question}

Return only one word:
dataset
superhero
both
"""

    try:
        response = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt
        )
    except Exception as exc:
        raise RuntimeError(
            "Gemini routing request failed."
        ) from exc

    route = response.output_text.strip().lower()

    if route not in {"dataset", "superhero", "both"}:
        raise RuntimeError(
            f"Gemini returned an invalid route: {route}"
        )

    return route