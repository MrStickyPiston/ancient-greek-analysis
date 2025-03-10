import csv
import unicodedata
import urllib.parse
from pprint import pprint
from typing import Tuple
import sys

import requests
from bs4 import BeautifulSoup

from data.scraping.noun_metadata import get_definitions, get_metadata


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
        "Masculine": 0,
        "Feminine": 1,
        "MasculineOrFeminine": 2,
        "Neuter": 3
    }
    return genders.get(str(gender_str), -1)

def get_tables(html, dialect="Attic"):
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
    dialect_tables = []

    for table in reversed(tables):
        div = table.find('div', class_='NavHead')
        if div:
            dialects = div.find_all('a', class_='extiw')
            for table_dialect in dialects:
                if table_dialect.text.strip() == dialect:
                    dialect_tables.append(table)

    return dialect_tables


def backup_get_gender(html):
    # Slightly less accurate gender for when no article is present
    gender_letters = []

    soup = BeautifulSoup(html, 'html.parser')
    gender_span = soup.find('span', class_='gender')
    if gender_span:
        gender_abbr = gender_span.find_all('abbr')
        for abbr in gender_abbr:
            gender_letters.append(abbr.text)

    return set(gender_letters)


def get_gender(html, table):
    # Detects gender based on article used in the table header. When no article is present the backup function backup_get_gender is used instead.
    table_articles = [a['title'] for a in table.find(class_='NavHead').find_all('a', title=True)]

    gender = set()

    for article in table_articles:
        if article in MASCULINE_ARTICLES:
            gender.add('m')
        elif article in FEMININE_ARTICLES:
            gender.add('f')
        elif article in NEUTER_ARTICLES:
            gender.add('n')

    if gender == set():
        gender = backup_get_gender(html)

    if gender == {'m'}:
        return "Masculine"
    elif gender == {'f'}:
        return "Feminine"
    elif gender == {'m', 'f'}:
        return "MasculineOrFeminine"
    elif gender == {'n'}:
        return "Neuter"
    else:
        print(f"Unknown gender: {gender} ({table.find(class_='NavHead').text.strip()})")
        return f"Unknown"


def get_root(table):
    def longest_substr(data):
        substr = ''

        word = data[0]

        if len(data) > 1 and len(word) > 0:
            for i in range(len(word)):
                for j in range(len(word) - i + 1):
                    if j > len(substr) and all(word[i:i + j] in x for x in data):
                        substr = word[i:i + j]

        return substr

    conjugations = []
    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])

        if cols[0].text == 'Case / #\n':
            amount_col = [column.text for column in cols]
        else:
            if cols[0].text == "Notes:\n":
                continue

            for i in range(1,len(amount_col)):
                cell = cols[i].find_all(class_='lang-grc')

                if not cell:
                    continue

                conjugations.append(without_accents(cell[-1].text))

    return longest_substr(conjugations)



ALLOWED_ACCENTS = [
    # Spiriti
    b'\xcc\x93'.decode(),
    b'\xcc\x94'.decode(),

    # Iota subscript
    b'\xcd\x85'.decode()
]

# Nominative articles
MASCULINE_ARTICLES = ['ὁ', 'οἱ']
FEMININE_ARTICLES = ['ἡ', 'αἱ']
NEUTER_ARTICLES = ['τὸ', 'τὼ', 'τὰ']
ARTICLES = MASCULINE_ARTICLES + FEMININE_ARTICLES + NEUTER_ARTICLES

def without_accents(s):
    return unicodedata.normalize(
        'NFC',
        ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c) or c in ALLOWED_ACCENTS)
    )

def get_conjugations(wiktionary_id):

    while True:
        try:
            html = requests.get(f'https://en.wiktionary.org/w/api.php?action=parse&page={wiktionary_id}&format=json').json()['parse']['text']['*']
            break
        except Exception as e:
            print(f"An error occured: {e}")
    tables = get_tables(html)

    if not tables:
        print(f"No conjugations found for {wiktionary_id}")
        return []

    conjugations = []

    for table in tables:
        nominative_singular = table.select_one('.NavContent .inflection-table-grc tbody tr:nth-child(2) td').find_all(class_='lang-grc')[-1].text

        gender = get_gender(html, table)
        root = get_root(table)
        if root is None:
            print(f"No root found for {wiktionary_id}")
            return []

        amount_col = []

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

                    word = without_accents(cell[-1].text)

                    # TODO: make this work with mutliple conjugations like vocative singular of https://en.wiktionary.org/wiki/%E1%BC%80%CE%B4%CE%B5%CE%BB%CF%86%CF%8C%CF%82#Ancient_Greek

                    try:
                        prefix = ''

                        if root == '' or len(word.split(root, 1)) == 1:
                            suffix = word
                        else:
                            prefix, suffix = word.split(root, 1)

                        conjugations.append((nominative_singular,
                                             root,
                                             prefix,
                                             suffix,
                                             word,
                                             gender,
                                             case.strip('\n'),
                                             amount_col[i].strip('\n'),
                                             get_metadata(wiktionary_id),
                                             wiktionary_id))
                    except ValueError:
                        print(f"WARNING: non-default root for conjugation: {word}. (wiktionary: {wiktionary_id}, root: {root})")
                        continue

    return conjugations

def url_to_id(url):
    # Returns id when an url is provided and else returns the input
    return urllib.parse.urlparse(url).path.split("/")[-1]

def main():
    conjugations = get_conjugations(url_to_id(input("Enter a wiktionary url or id: ")))

    csv.writer(sys.stdout).writerows(conjugations)

    # print()
    # print("INSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, metadata) VALUES")
    # print(f"\t('{root}', '{without_accents(root)}', '{nominative_singular}', {int_from_gender(gender)}, '{get_metadata(wiktionary_id)}')", end=",")

def from_file(file):
    conjugations = []

    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                conjugations += get_conjugations(word)
    except KeyboardInterrupt:
        pass

    with open(file.replace('.txt', '_parsed.csv'), mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(conjugations)

    print(f"Found {len(conjugations)} conjugations")

if __name__ == "__main__":
    main()
    from_file("data/raw/nouns/all.txt")