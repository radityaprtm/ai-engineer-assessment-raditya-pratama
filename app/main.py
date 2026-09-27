import json

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

from app.config import GEMINI_API_KEY
from app.superhero import search_superhero


app = FastAPI()

client = genai.Client(api_key=GEMINI_API_KEY)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Engineer Assessment"
    }


def extract_superhero_name(question: str):
    prompt = f"""
Extract the superhero or villain name from this question.

Question:
{question}

Return only the character name.
Do not explain anything.
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return response.output_text.strip()


@app.post("/ask")
def ask(request: AskRequest):
    hero_name = extract_superhero_name(request.question)

    heroes = search_superhero(hero_name)

    hero_data = json.dumps(heroes)

    prompt = f"""
Answer the user's question using only the SuperHero API data provided below.

Question:
{request.question}

SuperHero API data:
{hero_data}

If multiple characters match, explain that briefly.
Keep the answer concise.
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return {
        "answer": response.output_text,
        "sources": [
            {
                "type": "superhero_api",
                "name": "SuperHero API"
            }
        ]
    }