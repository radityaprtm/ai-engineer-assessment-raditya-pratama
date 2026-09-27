from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_empty_question_is_rejected():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_missing_question_is_rejected():
    response = client.post(
        "/ask",
        json={}
    )

    assert response.status_code == 422


def test_dataset_question_returns_answer_and_source():
    fake_gemini_response = SimpleNamespace(
        output_text="Apollo 11 landed on the Moon on July 20, 1969."
    )

    with patch(
        "app.main.classify_question",
        return_value="dataset"
    ), patch(
        "app.main.search_space_dataset",
        return_value=(
            "Apollo 11 landed on the Moon on July 20, 1969."
        )
    ), patch(
        "app.main.client.interactions.create",
        return_value=fake_gemini_response
    ):
        response = client.post(
            "/ask",
            json={
                "question": "When did Apollo 11 land on the Moon?"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "Apollo 11" in data["answer"]

    assert data["sources"] == [
        {
            "type": "dataset",
            "name": "data/space.txt"
        }
    ]

def test_both_sources_are_used():
    fake_gemini_response = SimpleNamespace(
        output_text="Iron Man and Apollo 11 use very different technologies."
    )

    fake_heroes = [
        {
            "id": "346",
            "name": "Iron Man",
            "powerstats": {
                "intelligence": "100",
                "strength": "85",
                "power": "100"
            },
            "biography": {
                "full-name": "Tony Stark"
            }
        }
    ]

    with patch(
        "app.main.classify_question",
        return_value="both"
    ), patch(
        "app.main.search_space_dataset",
        return_value="Apollo 11 used a Saturn V rocket."
    ), patch(
        "app.main.extract_superhero_name",
        return_value="Iron Man"
    ), patch(
        "app.main.search_superhero",
        return_value=fake_heroes
    ), patch(
        "app.main.client.interactions.create",
        return_value=fake_gemini_response
    ):
        response = client.post(
            "/ask",
            json={
                "question": (
                    "Compare Iron Man with the technology "
                    "used during Apollo 11."
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "Iron Man" in data["answer"]

    assert data["sources"] == [
        {
            "type": "dataset",
            "name": "data/space.txt"
        },
        {
            "type": "superhero_api",
            "name": "SuperHero API"
        }
    ]


def test_superhero_question_returns_answer_and_source():
    fake_gemini_response = SimpleNamespace(
        output_text="Batman has an intelligence score of 100."
    )

    fake_heroes = [
        {
            "id": "70",
            "name": "Batman",
            "powerstats": {
                "intelligence": "100"
            },
            "biography": {
                "full-name": "Bruce Wayne"
            }
        }
    ]

    with patch(
        "app.main.classify_question",
        return_value="superhero"
    ), patch(
        "app.main.extract_superhero_name",
        return_value="Batman"
    ), patch(
        "app.main.search_superhero",
        return_value=fake_heroes
    ), patch(
        "app.main.client.interactions.create",
        return_value=fake_gemini_response
    ):
        response = client.post(
            "/ask",
            json={
                "question": "How intelligent is Batman?"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "Batman" in data["answer"]

    assert data["sources"] == [
        {
            "type": "superhero_api",
            "name": "SuperHero API"
        }
    ]