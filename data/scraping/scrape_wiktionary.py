import csv
import unicodedata
import urllib.parse
from pprint import pprint
from typing import Tuple

import requests
from bs4 import BeautifulSoup


def int_from_amount(amount_str: str) -> int:
    amounts = {
        "Singular": 0,
        "Dual": 1,
        "Plural": 2
    }
    return amounts.get(amount_str, -1)

def int_from_case(case_str: str) -> int:
    cases = {
        "Nominative": 0,
        "Genitive": 1,
        "Dative": 2,
        "Accusative": 3,
        "Vocative": 4
    }
    return cases.get(case_str, -1)

def int_from_gender(gender_str: Tuple[str] | str) -> int:
    genders = {
        "('m',)": 0,
        "('f',)": 1,
        "('m', 'f')": 2,
        "('f', 'm')": 2,
        "('n',)": 3,
        "('m', 'pl')": 4,
        "('f', 'pl')": 5,
        "('m', 'f', 'pl')": 6,
        "('n', 'pl')": 7,
    }
    return genders.get(str(gender_str), -1)

def get_table(html, dialect="Attic"):
    """
    Scrapes a table with class "NavFrame grc-decl" containing a div with class "NavHead"
    and a link with class "extiw" and text "Attic" from the specified URL.

    In other words, finds the conjugation table from a wiktionary.org page

    Args:
        url (str): The URL to scrape.
        dialect (str): the dialect to choose

    Returns:
        The table element if found, otherwise None.
    """

    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('div', class_='NavFrame grc-decl')
    latest_table = None

    for table in reversed(tables):
        div = table.find('div', class_='NavHead')
        if div:
            dialects = div.find_all('a', class_='extiw')
            for table_dialect in dialects:
                if table_dialect.text.strip() == dialect:
                    latest_table = table
                    break

    return latest_table

def get_gender(html):
    gender_letters = []

    soup = BeautifulSoup(html, 'html.parser')
    gender_span = soup.find('span', class_='gender')
    if gender_span:
        gender_abbr = gender_span.find_all('abbr')
        for abbr in gender_abbr:
            gender_letters.append(abbr.text)

    return tuple(gender_letters)

def get_root(nominative_singular):
    for ending in NOMINATIVE_SINGULAR_ENDINGS:
        if without_accents(nominative_singular).endswith(ending):

            # reverse for
            n = 0
            for i in range(len(nominative_singular)-1, -1, -1):
                char = nominative_singular[i]

                if not unicodedata.combining(char):
                    n += 1
                    if n == len(ending):
                        return nominative_singular[:i]



ALLOWED_ACCENTS = [
    # Spiriti
    b'\xcc\x93'.decode(),
    b'\xcc\x94'.decode(),

    # Iota subscript
    b'\xcd\x85'.decode()
]

# Order does matter
NOMINATIVE_SINGULAR_ENDINGS = [
    "ος",
    "α",
    "η",
    "ης",
    "αι",
    "ας",
    "οι",
    "ον",
    "ευς",
    "ους",
    "ες",
    "ως"
]

def without_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c) or c in ALLOWED_ACCENTS)

def get_conjugations(wiktionary_id):
    url = id_to_url(wiktionary_id)

    while True:
        try:
            html = requests.get(url).text
            break
        except Exception as e:
            print(f"An error occured: {e}")
    table = get_table(html)

    if not table:
        print(f"No conjugations found for {wiktionary_id}")
        return []

    nominative_singular = table.select_one('.NavContent .inflection-table-grc tbody tr:nth-child(2) td').find_all(class_='lang-grc')[-1].text

    gender = get_gender(html)
    root = get_root(nominative_singular)
    if root is None:
        print(f"No root found for {wiktionary_id}")
        return []

    # print(f"Using gender: {",".join(gender)} and root: {root} for {wiktionary_id}")

    amount_col = []
    conjugations = []

    # Extract data from the table
    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])

        if cols[0].text == 'Case / #\n':
            amount_col = [column.text for column in cols]
        else:
            case = cols[0].text

            if case == "Notes:\n":
                continue

            for i in range(1,len(amount_col)):
                cell = cols[i].find_all(class_='lang-grc')

                if not cell:
                    continue

                word = cell[-1].text

                # TODO: make this work with mutliple conjugations like vocative singular of https://en.wiktionary.org/wiki/%E1%BC%80%CE%B4%CE%B5%CE%BB%CF%86%CF%8C%CF%82#Ancient_Greek

                try:
                    prefix, suffix = word.split(root)
                    conjugations.append((nominative_singular,
                                         root, without_accents(root),
                                         prefix, without_accents(prefix),
                                         suffix, without_accents(suffix),
                                         word, without_accents(word),
                                         gender,
                                         case.strip('\n'),
                                         amount_col[i].strip('\n'),
                                         True,
                                         wiktionary_id))
                except ValueError:

                    try:
                        prefix, suffix = without_accents(word).split(without_accents(root))

                        prefix = word[:len(prefix)]
                        suffix = word[len(word) - len(suffix):]

                        # print(f"WARNING: root with different accent for conjugation '{word}'. Using prefix '{prefix}' and suffix '{suffix}', but a manual check is recommended.")

                        # different accents, not exact
                        conjugations.append((nominative_singular,
                                             root, without_accents(root),
                                             prefix, without_accents(prefix),
                                             suffix, without_accents(suffix),
                                             word, without_accents(word),
                                             gender,
                                             case.strip('\n'),
                                             amount_col[i].strip('\n'),
                                             False,
                                             wiktionary_id))
                    except ValueError:
                        print(f"WARNING: non-default root for conjugation: {word}. Exiting.")
                        return []
    return conjugations

def url_to_id(url):
    # Returns id when an url is provided and else returns the input
    return urllib.parse.urlparse(url).path.split("/")[-1]

def id_to_url(wiktionary_id):
    return "https://en.wiktionary.org/wiki/" + wiktionary_id

def main():
    conjugations = get_conjugations(url_to_id(input("Enter a wiktionary url or id: ")))

    pprint(conjugations, compact=True, width=120)

    # print()
    # print("INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, metadata) VALUES")
    # print(f"\t('{root}', '{without_accents(root)}', '{nominative_singular}', {int_from_gender(gender)}, '{get_metadata(wiktionary_id)}')", end=",")

def from_file(file):
    conjugations = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            conjugations += get_conjugations(word)

    with open(file.replace('.txt', '_parsed.csv'), mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(conjugations)

    print(f"Found {len(conjugations)} conjugations")

if __name__ == "__main__":
    from_file("data/raw/ancient_greek_second-declension_nouns.txt")