import json

from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.retriever import search_space_dataset
from app.router import classify_question
from app.superhero import search_superhero
from app.models import AskRequest, AskResponse


app = FastAPI()

client = genai.Client(api_key=GEMINI_API_KEY)


# class AskRequest(BaseModel):
#     question: str = Field(
#         min_length=2,
#         max_length=500
#     )


# @app.get("/")
# def home():
#     return {
#         "message": "AI Engineer Assessment"
#     }


def extract_superhero_name(question: str):
    prompt = f"""
Extract one superhero or villain search name from the user's question.

Use the character's commonly known superhero or villain name.
If the user provides a civilian identity and its superhero identity is
unambiguous, return the superhero name instead.

Examples:
Question: How clever is Tony Stark?
Search name: Iron Man

Question: How clever is Iron Man?
Search name: Iron Man

If you cannot confidently identify the character, preserve the supplied
name rather than inventing a different character.

Return only the search name, without quotation marks or explanations.

Question:
{question}
"""

    try:
        response = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt
        )
    except Exception as exc:
        raise RuntimeError(
            "Gemini superhero extraction request failed."
        ) from exc

    return response.output_text.strip()


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        route = classify_question(request.question)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

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
        try:
            hero_name = extract_superhero_name(request.question)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail=str(exc)
            )

        try:
            heroes = search_superhero(hero_name)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=502,
                detail=str(exc)
            )

        if heroes:
            hero_data = json.dumps(heroes)

            contexts.append(
                f"SuperHero API data:\n{hero_data}"
            )
        else:
            contexts.append(
                f"SuperHero API returned no results for: {hero_name}"
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

    try:
        response = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Gemini answer generation failed."
        ) from exc

    return {
        "answer": response.output_text,
        "sources": sources
    }