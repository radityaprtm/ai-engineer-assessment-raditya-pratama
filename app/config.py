import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPERHERO_API_TOKEN = os.getenv("SUPERHERO_API_TOKEN")

GEMINI_MODEL = "gemini-3.1-flash-lite"