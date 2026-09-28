import re
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "space.txt"
)


STOP_WORDS = {
    "a", "an", "and", "are", "did", "does", "for",
    "how", "in", "is", "of", "on", "the", "to",
    "was", "were", "what", "when", "where", "who", "why"
}


def get_words(text: str):
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def search_space_dataset(question: str) -> str | None:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    sections = text.split("\n\n")

    question_words = get_words(question)

    best_section = None
    best_score = 0

    for section in sections:
        section_words = get_words(section)

        matching_words = question_words & section_words
        score = len(matching_words)

        if score > best_score:
            best_score = score
            best_section = section

    if best_score == 0:
        return None

    return best_section