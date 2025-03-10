import sys

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

    print("\nWARNING: no ancient greek definition found")

    return []

def get_metadata(wiktionary_id):
    return str({
        'wiktionary_id': wiktionary_id,
        'definitions': get_definitions(wiktionary_id)
    }).replace("'", '"')

def main(folder):
    with open(folder + 'index.txt') as f:
        pages = f.read().splitlines()
        print(f"Parsing {len(pages)} pages")

        results = {}
        for page in pages:
            results[page] = get_metadata(page)
            print(f"\rProgress: {len(results)}/{len(pages)}", end="")

        with open(folder + 'definitions.json', 'w') as f:
            json.dump(results, f)

if __name__ == "__main__":
    main(sys.argv[1])
