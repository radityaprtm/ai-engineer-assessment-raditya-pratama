import json

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

from app.superhero import search_superhero
from app.config import GEMINI_API_KEY


app = FastAPI()

client = genai.Client(api_key=GEMINI_API_KEY)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Engineer Assessment"
    }


@app.post("/ask")
def ask(request: AskRequest):
    heroes = search_superhero(request.question)

    hero_data = json.dumps(heroes)

    prompt = f"""
Answer the user's superhero question using only the SuperHero API data below.

User question:
{request.question}

SuperHero API data:
{hero_data}

If multiple characters match the name, mention the ambiguity.
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