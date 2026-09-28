import pytest

from pydantic import ValidationError

from app.models import AskRequest


@pytest.mark.parametrize(
    "question",
    [
        "",
        "   ",
        "\n\t",
        "a",
        None,
        123,
        "x" * 501,
    ],
)
def test_invalid_question_is_rejected(question):
    with pytest.raises(ValidationError):
        AskRequest(question=question)


def test_question_is_trimmed():
    request = AskRequest(
        question="   Who is Batman?   "
    )

    assert request.question == "Who is Batman?"


def test_500_character_question_is_accepted():
    request = AskRequest(question="x" * 500)

    assert len(request.question) == 500


def test_unexpected_field_is_rejected():
    with pytest.raises(ValidationError):
        AskRequest(
            question="Who is Batman?",
            unexpected_field=True,
        )