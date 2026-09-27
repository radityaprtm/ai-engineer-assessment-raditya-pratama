import json

from fastapi import FastAPI
from pydantic import BaseModel, Field
from google import genai

from app.config import GEMINI_API_KEY
from app.retriever import search_space_dataset
from app.router import classify_question
from app.superhero import search_superhero


app = FastAPI()

client = genai.Client(api_key=GEMINI_API_KEY)


from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=500
    )

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
    route = classify_question(request.question)

    contexts = []
    sources = []

    if route == "dataset" or route == "both":
        space_context = search_space_dataset(request.question)

        contexts.append(
            f"Space dataset:\n{space_context}"
        )

        sources.append({
            "type": "dataset",
            "name": "data/space.txt"
        })

    if route == "superhero" or route == "both":
        hero_name = extract_superhero_name(request.question)

        heroes = search_superhero(hero_name)

        hero_data = json.dumps(heroes)

        contexts.append(
            f"SuperHero API data:\n{hero_data}"
        )

        sources.append({
            "type": "superhero_api",
            "name": "SuperHero API"
        })

    context_text = "\n\n".join(contexts)

    prompt = f"""
Answer the user's question using only the information provided below.

Question:
{request.question}

Information:
{context_text}

If the information is ambiguous or incomplete, say so.
Keep the answer concise.
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return {
        "answer": response.output_text,
        "sources": sources
    }