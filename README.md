# AI Engineer Assessment

This is a FastAPI chatbot that answers questions using:
- Local text dataset about space exploration
- Superhero API
- Both sources when prompted

The project features Google Gemini to classify questions and generate answers from the retrieved information

## Setup
Clone the repository:

git clone https://github.com/radityaprtm/ai-engineer-assessment-raditya-pratama.git

### Create and activate a virtual environment
python -m venv .venv

### Windows powershell:
.venv\Scripts\Activate.ps1

### macOS / Linux Terminal

Create a virtual environment, install dependencies, and create your local
configuration file:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

### Install dependencies
pip install -r requirements.txt

- (Requires Python with `pip` and `venv`, Git, a Gemini API key, and a SuperHero API token.)

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
For example a request:
{
    question: "What is Apollo 11?"
}
```

```
A mixed source request:

{
  "question": "When did Apollo 11 land on the Moon, and what is Tony Stark'\''s intelligence score?"
}

```


Every response includes the source or sources used to produce the answer.

### Example of Responses:

```
{
  "answer": "Apollo 11 was the first crewed mission to land humans on the Moon, launched by NASA on July 16, 1969. During the mission, Neil Armstrong and Buzz Aldrin landed the lunar module Eagle on the Moon on July 20, 1969, while Michael Collins remained in lunar orbit. Armstrong became the first person to walk on the Moon.",
  "sources": [
    {
      "type": "dataset",
      "name": "data/space.txt"
    }
  ]
}
```


```
{
  "answer": "Apollo 11 landed on the Moon on July 20, 1969. Tony Stark's intelligence score is 100.",
  "sources": [
    {
      "type": "dataset",
      "name": "data/space.txt"
    },
    {
      "type": "superhero_api",
      "name": "SuperHero API"
    }
  ]
}
```

### Tests

Run the automated tests from the project directory.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

**macOS / Linux:**

```bash
./.venv/bin/python -m pytest -v
```

Tested with Python 3.14.7 on Windows