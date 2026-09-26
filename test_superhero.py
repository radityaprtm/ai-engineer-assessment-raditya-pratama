from app.superhero import search_superhero

heroes = search_superhero("batman")

for hero in heroes:
    print(
        hero["name"],
        "-",
        hero["biography"]["full-name"]
    )

