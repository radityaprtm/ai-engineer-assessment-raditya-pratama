from unittest.mock import Mock, patch

import httpx
import pytest

from app.superhero import search_superhero


def test_superhero_search_returns_results():
    fake_response = Mock()

    fake_response.json.return_value = {
        "response": "success",
        "results": [
            {
                "id": "70",
                "name": "Batman"
            }
        ]
    }

    with patch(
        "app.superhero.httpx.get",
        return_value=fake_response
    ):
        results = search_superhero("Batman")

    assert len(results) == 1
    assert results[0]["name"] == "Batman"


def test_superhero_not_found_returns_empty_list():
    fake_response = Mock()

    fake_response.json.return_value = {
        "response": "error",
        "error": "character with given name not found"
    }

    with patch(
        "app.superhero.httpx.get",
        return_value=fake_response
    ):
        results = search_superhero("Super Banana Man 9000")

    assert results == []


def test_superhero_api_error_raises_runtime_error():
    fake_response = Mock()

    fake_response.json.return_value = {
        "response": "error",
        "error": "invalid access token"
    }

    with patch(
        "app.superhero.httpx.get",
        return_value=fake_response
    ):
        with pytest.raises(
            RuntimeError,
            match="SuperHero API error"
        ):
            search_superhero("Batman")


def test_superhero_network_failure_raises_runtime_error():
    with patch(
        "app.superhero.httpx.get",
        side_effect=httpx.ConnectError("Connection failed")
    ):
        with pytest.raises(
            RuntimeError,
            match="SuperHero API request failed"
        ):
            search_superhero("Batman")