import csv
import unicodedata
from pprint import pprint
from typing import Tuple
import sys
import json

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import without_accents

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

def get_gender(html, table):
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

    MASCULINE_ARTICLES = ['ὁ', 'οἱ']
    FEMININE_ARTICLES = ['ἡ', 'αἱ']
    NEUTER_ARTICLES = ['τὸ', 'τὼ', 'τὰ']
    ARTICLES = MASCULINE_ARTICLES + FEMININE_ARTICLES + NEUTER_ARTICLES

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
        print(f"\nUnknown gender: {gender} ({table.find(class_='NavHead').text.strip()})")
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

def get_conjugations(wiktionary_id, definitions, folder):

    html = open(folder + wiktionary_id + ".html", 'r').read()
    tables = get_tables(html)

    if not tables:
        print(f"\nNo conjugations found for {wiktionary_id}")
        return []

    conjugations = []

    for table in tables:
        gender = get_gender(html, table)
        root = get_root(table)
        if root is None:
            print(f"\nNo root found for {wiktionary_id}")
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

                        conjugations.append((wiktionary_id,
                                             root,
                                             prefix,
                                             suffix,
                                             word,
                                             gender,
                                             case.strip('\n'),
                                             amount_col[i].strip('\n'),
                                             definitions.get(wiktionary_id)
                                             ))
                    except ValueError:
                        print(f"\nWARNING: non-default root for conjugation: {word}. (wiktionary: {wiktionary_id}, root: {root})")
                        continue

    return conjugations

def main(folder):
    with open(folder + "index.txt") as f:
        pages = f.read().splitlines()

    print(f"Parsing {len(pages)} pages")

    conjugations = []
    processes = []

    with open(folder + 'definitions.json', 'r') as file:
        definitions = json.load(file)

    with ThreadPoolExecutor(max_workers=None) as executor:
        for page in pages:
            processes.append(executor.submit(get_conjugations, page, definitions, folder))

        i = 0

        for result in as_completed(processes):
            i += 1
            print(f"\rProgress: {i}/{len(pages)}", end="")
            conjugations += result.result()

    with open(folder + "parsed.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(conjugations)


if __name__ == "__main__":
    main(sys.argv[1])