import sys

from app.retriever import search_space_dataset


question = "What is Voyager 1"

result = search_space_dataset(question)

print(result)