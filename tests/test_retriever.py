from app.retriever import search_space_dataset


def test_apollo_question_returns_apollo_section():
    result = search_space_dataset(
        "When did Apollo 11 land on the Moon?"
    )

    assert result is not None
    assert "Apollo 11" in result
    assert "July 20, 1969" in result


def test_voyager_question_returns_voyager_section():
    result = search_space_dataset(
        "What is Voyager 1?"
    )

    assert result is not None
    assert "Voyager 1" in result
    assert "interstellar space" in result

def test_unrelated_question_returns_none():
    result = search_space_dataset(
        "What is the capital city of France?"
    )

    assert result is None