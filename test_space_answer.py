from google import genai

from app.config import GEMINI_API_KEY
from app.retriever import search_space_dataset


client = genai.Client(api_key=GEMINI_API_KEY)

question = "What is Voyager 1?"

context = search_space_dataset(question)

prompt = f"""
Answer the question using only the dataset context provided below.

Question:
{question}

Dataset context:
{context}

Keep the answer concise.
"""

response = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt
)

print(response.output_text)
print("Source: data/space.txt")