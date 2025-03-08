import re
import urllib.parse
import requests
from bs4 import BeautifulSoup


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

def main():
    url = input("Enter a wiktionary.org url: ")
    wiktionary_id = urllib.parse.urlparse(url).path.split("/")[-1]

    print(f", '{get_metadata(wiktionary_id)}'", end="")

if __name__ == "__main__":
    main()