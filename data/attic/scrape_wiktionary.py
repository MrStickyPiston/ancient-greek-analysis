from pprint import pprint

import requests
from bs4 import BeautifulSoup

import re

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

def int_from_gender(gender_str: str) -> int:
    genders = {
        "Masculine": 0,
        "Feminine": 1,
        "MasculineOrFeminine": 2,
        "Neuter": 3
    }
    return genders.get(gender_str, -1)

def get_table(url, dialect="Attic"):
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

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

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

# HTML source with a table
html_source = open('table').read()
# gender_id = input("Enter the gender ID: ")
# root = input("Enter the root: ")

table = get_table(input("Enter a wiktionary.org url: "))
nominative_singular = table.select_one('.NavContent .inflection-table-grc tbody tr:nth-child(2) td').find_all(class_='lang-grc')[-1].text
root = input(f"Found a table with nominative singular {nominative_singular}. Enter the root: ")
gender = input("Enter the gender: ")

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

            try:
                prefix, suffix = word.split(root)
            except ValueError:
                print(f"WARNING: non-default root for conjugation: {word}. Skipping conjugation.")
                continue

            conjugations.append(f"('{nominative_singular}', '{prefix}', '{suffix}', {int_from_amount(amount_col[i].strip('\n'))}, {int_from_case(case.strip('\n'))}, {int_from_gender(gender)})")

print("Run the following SQL code to add this to the database:\n")
print("INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, morphological_amount, morphological_case, morphological_gender) VALUES")
for c in range(len(conjugations)):
    print("\t", end="")
    print(conjugations[c], end="")

    if c < len(conjugations) - 1:
        print(",")
    else:
        print(";")