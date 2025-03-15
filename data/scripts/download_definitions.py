import sys

import requests
from bs4 import BeautifulSoup
import json
import os

def get_definitions(wiktionary_id):
    r = requests.get(f"https://en.wiktionary.org/api/rest_v1/page/definition/{wiktionary_id}")

    if r.status_code == 404:
        print(f"\nDefinition not found for {wiktionary_id}")
        return []
    r.raise_for_status()

    try:
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
    except KeyError:
        print(f"\nAncient Greek definition not found for {wiktionary_id}")
        return []

    print("\nWARNING: no ancient greek definition found")

    return []

def get_metadata(wiktionary_id):
    return str({
        'wiktionary_id': wiktionary_id,
        'definitions': get_definitions(wiktionary_id)
    }).replace("'", '"')

def main(folder):
    old = {}

    if os.path.exists(folder + 'definitions.json'):
        with open(folder + 'definitions.json', 'r') as f:
            old = json.load(f)

    with open(folder + 'index.txt') as f:
        pages = f.read().splitlines()
        print(f"Downloading {len(pages)} definitions")

        new = {}
        try:
            for page in pages:

                if not old.get(page):
                    new[page] = get_metadata(page)

                print(f"\rProgress: {len(new) + len(old)}/{len(pages)}", end="")
        except BaseException as e:
            print(f"An error occured:")
            print(e)

    with open(folder + 'definitions.json', 'w') as f:
        results = old.copy()
        results.update(new)
        json.dump(results, f)

if __name__ == "__main__":
    main(sys.argv[1])
