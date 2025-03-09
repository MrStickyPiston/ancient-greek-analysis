import requests
from bs4 import BeautifulSoup
import json

def get_definitions(wiktionary_id):
    r = requests.get(f"https://en.wiktionary.org/api/rest_v1/page/definition/{wiktionary_id}")
    r.raise_for_status()

    for item in r.json()["other"]:
        if item["language"].lower() == "ancient greek":

            definitions = []

            for i in item["definitions"]:
                definition = i['definition']
                soup = BeautifulSoup(definition, 'html.parser')

                text = soup.get_text()

                for d in text.split("\n"):
                    if d.strip() != "":
                        definitions.append(d.strip())

            return definitions

    print("WARNING: no ancient greek definition found")

    return []

def get_metadata(wiktionary_id):
    return str({
        'wiktionary_id': wiktionary_id,
        'definitions': get_definitions(wiktionary_id)
    }).replace("'", '"')


with open('/home/sticky/coding/ancient-greek-analysis/data/scripts/data/nouns/proper/index.txt') as f:
    pages = f.read().splitlines()
    print(f"Parsing {len(pages)} pages")

    results = {}
    for page in pages:
        results[page] = get_metadata(page)
        print(f"\rProgress: {len(results)}/{len(pages)}", end="")

    with open('/home/sticky/coding/ancient-greek-analysis/data/scripts/data/nouns/proper/definitions.json', 'w') as f:
        json.dump(results, f)

