from fastapi import FastAPI
from pydantic import BaseModel

#import google library:
from google import genai

app = FastAPI()

client = genai.Client()


class AskRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "AI Engineer Assessment"}

@app.post("/ask")
def ask(request: AskRequest):

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=request.question
    )

    return {
        "answer": response.output_text,
        "sources": [
            {
                "type": "llm",
                "name": "Google Gemini"
            }
        ]
    }