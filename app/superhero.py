import httpx

from app.config import SUPERHERO_API_TOKEN


def search_superhero(name: str):
    token = SUPERHERO_API_TOKEN

    if not token:
        raise RuntimeError("SUPERHERO_API_TOKEN is not set.")

    url = f"https://superheroapi.com/api/{token}/search/{name}"

    try:
        response = httpx.get(
            url,
            timeout=10.0,
            follow_redirects=True
        )

        response.raise_for_status()

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "SuperHero API request failed."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "SuperHero API returned invalid JSON."
        ) from exc

    return data.get("results", [])