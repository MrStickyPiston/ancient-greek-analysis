import unicodedata
import urllib.parse
from typing import Tuple

import requests
from bs4 import BeautifulSoup

from data.scraping.noun_metadata import get_metadata


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

def int_from_gender(gender_str: Tuple[str]) -> int:
    genders = {
        ('m',): 0,
        ('f',): 1,
        ('m','f'): 2,
        ('n',): 3
    }
    return genders.get(gender_str, -1)

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
            extiw = div.find('a', class_='extiw')
            if extiw and extiw.text.strip() == dialect:
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
            return nominative_singular[:-len(ending)]


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
    "α"
]

def without_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c) or c in ALLOWED_ACCENTS)


url = input("Enter a wiktionary.org url: ")
wiktionary_id = urllib.parse.urlparse(url).path.split("/")[-1]

html = requests.get(url).text
table = get_table(html)
nominative_singular = table.select_one('.NavContent .inflection-table-grc tbody tr:nth-child(2) td').find_all(class_='lang-grc')[-1].text

gender = get_gender(html)
root = get_root(nominative_singular)
print(f"Using gender: {",".join(gender)} and root: {root}")

exact = 'true'

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
            word = cols[i].find_all(class_='lang-grc')[-1].text
            # TODO: make this work with mutliple conjugations like vocative singular of https://en.wiktionary.org/wiki/%E1%BC%80%CE%B4%CE%B5%CE%BB%CF%86%CF%8C%CF%82#Ancient_Greek

            try:
                prefix, suffix = word.split(root)
                conjugations.append(f"('{nominative_singular}', '{prefix}', '{suffix}', '{without_accents(prefix)}', '{without_accents(suffix)}', {int_from_amount(amount_col[i].strip('\n'))}, {int_from_case(case.strip('\n'))}, true)")
            except ValueError:

                try:
                    prefix, suffix = without_accents(word).split(without_accents(root))

                    prefix = word[:len(prefix)]
                    suffix = word[len(word) - len(suffix):]

                    print(f"WARNING: root with different accent for conjugation '{word}'. Using prefix '{prefix}' and suffix '{suffix}', but a manual check is recommended.")

                    # different accents, not exact
                    conjugations.append(f"('{nominative_singular}', '{prefix}', '{suffix}', '{without_accents(prefix)}', '{without_accents(suffix)}', {int_from_amount(amount_col[i].strip('\n'))}, {int_from_case(case.strip('\n'))}, false)")
                except ValueError:
                    print(f"WARNING: non-default root for conjugation: {word}. Exiting.")
                    exit(1)

print("Run the following SQL code to add this to the database:\n")
print("INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, prefix_without_accents, suffix_without_accents, morphological_amount, morphological_case, exact) VALUES")
for c in range(len(conjugations)):
    print("\t", end="")
    print(conjugations[c], end="")

    if c < len(conjugations) - 1:
        print(",")
    else:
        print(";")

print()
print("INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, metadata) VALUES")
print(f"\t('{root}', '{without_accents(root)}', '{nominative_singular}', {int_from_gender(gender)}, '{get_metadata(wiktionary_id)}')", end=",")