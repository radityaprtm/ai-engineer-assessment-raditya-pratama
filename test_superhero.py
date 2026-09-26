from app.superhero import search_superhero

heroes = search_superhero("batman")

for hero in heroes:
    print(
        hero["name"],
        "-",
        hero["biography"]["full-name"]
    )


# import os
# import httpx

# token = os.getenv("SUPERHERO_API_TOKEN")

# if not token:
#     raise SystemExit("SUPERHERO_API_TOKEN is not set in this terminal.")

# url = f"https://superheroapi.com/api/{token}/search/batman"

# response = httpx.get(
#     url,
#     timeout=10.0,
#     follow_redirects=True
# )

# data = response.json()

# results = data.get("results", [])

# for hero in results:
#     print(
#         hero["id"],
#         hero["name"],
#         "-",
#         hero["biography"]["full-name"]
#     )

# # print("Status:", response.status_code)
# # print("Content type:", response.headers.get("content-type"))

# # # check redirect
# # location = response.headers.get("location", "")
# # print("Redirect location:", location.replace(token, "[REDACTED]"))

# # # debug reply
# # safe_text = response.text.replace(token, "[****]")
# # print("Body preview:", repr(safe_text[:300]))