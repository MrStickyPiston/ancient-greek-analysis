import requests
import os

API_URL = "https://en.wiktionary.org/w/api.php"

def get_category(category):
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmtype": "page",
        "cmlimit": "500",
        "format": "json"
    }

    session = requests.Session()
    ids = []
    continue_params = {}

    while True:
        query_params = params.copy()
        query_params.update(continue_params)

        response = session.get(API_URL, params=query_params)
        data = response.json()

        category_members = data.get("query", {}).get("categorymembers", [])

        # Save each pageid as a string
        for member in category_members:
            ids.append(str(member["title"]))

        print(f"\rProgress for {category}: {len(ids)}", end="")

        # Check if there is a continuation token for more results
        if "continue" in data:
            continue_params = data["continue"]
        else:
            break  # No further data

    print()

    return ids

folder = "data/raw/nouns/"

ids = get_category("Category:Ancient_Greek_nouns")
os.makedirs(folder, exist_ok=True)
with open(folder + "all.txt", 'w') as file:
    for id in ids:
        file.write(id + "\n")

ids = get_category("Category:Ancient_Greek_proper_nouns")
with open(folder + "proper.txt", 'w') as file:
    for id in ids:
        file.write(id + "\n")
