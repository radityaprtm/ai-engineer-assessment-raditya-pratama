from google import genai

from app.config import GEMINI_API_KEY


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

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return response.output_text.strip().lower()