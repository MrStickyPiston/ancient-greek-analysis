import csv
import json
import re
import sys
from pprint import pprint

import pandas as pd
import numpy as np

from utils import without_accents


def get_amount(tags):
    for tag in tags:
        if tag in ['singular', 'dual', 'plural']:
            return tag

    return 'unknown'

def get_case(tags):
    for tag in tags:
        if tag in ['nominative', 'genitive', 'dative', 'accusative', 'vocative']:
            return tag

    return 'unknown'

def get_gender(tags):
    for tag in tags:
        if tag in ['masculine', 'feminine', 'neuter']:
            return tag

    return 'unknown'

def longest_substr(data):
    substr = ''

    word = data[0]

    if len(data) > 1 and len(word) > 0:
        for i in range(len(word)):
            for j in range(len(word) - i + 1):
                if j > len(substr) and all(word[i:i + j] in x for x in data):
                    substr = word[i:i + j]

    return substr

def process_conjugations(conjugations):
    # This functions takes a conjugation that contains the full word and outputs a version with a root and prefixes+suffixes
    words = [conjugation[1] for conjugation in conjugations]

    root = longest_substr(words)

    processed = []

    for conjugation in conjugations:
        if root == '':
            prefix = ''
            suffix = conjugation[1]
        else:
            prefix, suffix = conjugation[1].split(root, 1)

        processed.append((conjugation[0], root, prefix, suffix, word, conjugation[2], conjugation[3], conjugation[4], conjugation[5]))

    return processed

def head_template_to_gender(template):
    # Constructs the gender of a word out of the template header
    args_content = template.get('args').values()

    gender = set()

    for value in args_content:
        if value.replace('-p', '') in ['m', 'f', 'n']:
            gender.add(value.replace('-p', ''))

    if gender == {'m'}:
        return "masculine"
    elif gender == {'m', 'f'}:
        return "masculine/feminine"
    elif gender == {'f'}:
        return "feminine"
    elif gender == {'n'}:
        return "neuter"
    elif gender == {'m', 'n'}:
        return "masculine/neuter"
    else:
        print(f"Invalid gender: {gender} from template {template}")

# Download from https://kaikki.org/dictionary/Ancient%20Greek/kaikki.org-dictionary-AncientGreek.jsonl
df = pd.read_json(path_or_buf='data/kaikki.jsonl', lines=True)
print(df['pos'].unique())

# The articles will be stripped out of the conjugations later
articles = [
    'τῃσιν',
    'τῃσι',
    'της',
    'την',
    'τῃ',

    'οἱ',
    'ὁ',

    'ἡ',

    'αἱ',
    'ἁ',

    'ταις',
    'ται',
    'τας',
    'ταν',
    'τᾳ',
    'τα',

    'τοισιν',
    'τοις',
    'τοιν',
    'τοι',
    'το',

    'τους',
    'του',
    'τον',

    'των',
    'τως',
    'τῳ',
    'τω'
]
# The dialects that will be parsed
dialects = [
    'att'
]

# Store a list of all current conjugations
conjugations_list = []

for index, row in df.loc[df['pos'].isin(['noun', 'adj'])].iterrows():
    if not isinstance(row['forms'], list):
        continue

    if not any(form.get("source") == "declension" for form in row.forms):
        continue

    gender = None
    if isinstance(row.head_templates, list):
        gender = head_template_to_gender(row.head_templates[0])

    # Obtain definitions
    definitions = []
    for sense in row.senses:
        if sense.get('tags') and 'no-gloss' in sense['tags']:
            # No definition
            continue

        definitions += sense['glosses']

    conjugations = []

    # List of all conjugations for this word
    i = 0

    for form in row.forms:

        if 'table-tags' in form.get('tags'):
            # A new declension table starts here
            if conjugations:
                conjugations_list += process_conjugations(conjugations)
                i += 1

            conjugations = []
            continue

        if 'inflection-template' in form.get('tags') or 'class' in form.get('tags'):
            continue

        if 'adverbial' in form.get('tags') or 'comparative' in form.get('tags') or 'superlative' in form.get('tags'):
            # Ignore "Derived forms" of adjectives
            continue

        if isinstance(row.inflection_templates, list) and row.inflection_templates[i].get('args').get('dial', 'att') not in dialects:
            continue

        if form.get('source') == 'declension' and form['form'] != '-':
            word = without_accents(form['form'].strip())

            for article in articles:
                if word.startswith(article + " ") or word == article:
                    word = word[len(article):].strip()
                    break

            if word == "":
                continue

            if not re.match(r'^[\u0370-\u03FF\u1F00-\u1FFF]+$', word):
                # print(f"Warning: invalid characters in word {word} of group {row.word}{i}")
                continue

            if gender:
                conjugations.append((f"{row.word}{i}", word, gender, get_case(form['tags']), get_amount(form['tags']), {'wiktionary_id': row.word, 'definitions': definitions}))
            else:
                conjugations.append((f"{row.word}{i}", word, get_gender(form['tags']), get_case(form['tags']), get_amount(form['tags']), {'wiktionary_id': row.word, 'definitions': definitions}))

    # End of the last conjugation
    if conjugations:
        conjugations_list += process_conjugations(conjugations)

with open("data/parsed.csv", mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(conjugations_list)