from app.router import classify_question


questions = [
    "How intelligent is Batman?",
    "When did Apollo 11 land on the Moon?",
    "Compare Iron Man with the technology used during Apollo 11."
]


for question in questions:
    result = classify_question(question)

    print(question)
    print("Route:", result)
    print()