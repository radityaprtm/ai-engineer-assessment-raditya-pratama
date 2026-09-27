# AI Engineer Assessment

This is a FastAPI chatbot that answers questions using:
-Local text dataset about space exploration
-Superhero API
-Both sources when prompted

The project features Google Gemini to classify questions and generate answers from the retrieved information

## Setup
Clone the repository:

git clone https://github.com/radityaprtm/ai-engineer-assessment-raditya-pratama.git

### Create and activate a virtual environment
python -m venv .venv

Windows powershell:
.venv\Scripts\Activate.ps1

### Install dependencies
pip install -r requirements.txt

### Create environment file
Copy-Item .env.example .env

### Add API keys to .env
- GEMINI_API_KEY=your_gemini_api_key
- SUPERHERO_API_TOKEN=your_superhero_api_token
- GEMINI_MODEL=gemini-3.1-flash-lite

### Run:
uvicorn app.main:app --reload

### Open the FastAPI documentation at:
http://127.0.0.1:8000/docs

the chatbot exposes:
POST /ask

```
For example a request:
{
    question: "How intelligent is Batman?"
}
```

```
A mixed source request:

{
  "question": "Compare Iron Man with the technology used during Apollo 11."
}

```
Every response includes the source or sources used to produce the answer.

### Tests
python -m pytest -v