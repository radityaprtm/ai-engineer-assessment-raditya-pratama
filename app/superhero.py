import os
import httpx


def search_superhero(name: str):
    token = os.getenv("SUPERHERO_API_TOKEN")

    if not token:
        raise RuntimeError("SUPERHERO_API_TOKEN is not set.")

    url = f"https://superheroapi.com/api/{token}/search/{name}"

    response = httpx.get(
        url,
        timeout=10.0,
        follow_redirects=True
    )

    data = response.json()

    return data.get("results", [])