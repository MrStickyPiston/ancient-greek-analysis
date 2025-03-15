import json
import re
import sys
from pprint import pprint

import pandas as pd
import numpy as np

from utils import without_accents


def get_amount(tags):
    if tags[0] in ['singular', 'dual', 'plural']:
        return tags[0]
    else:
        return tags[1]

def get_case(tags):
    if tags[0] in ['singular', 'dual', 'plural']:
        return tags[1]
    else:
        return tags[0]

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
    words = [conjugation[2] for conjugation in conjugations]

    root = longest_substr(words)

    processed = []

    for conjugation in conjugations:
        if root == '':
            prefix = ''
            suffix = conjugation[2]
        else:
            prefix, suffix = conjugation[2].split(root, 1)

        processed.append((conjugation[0], conjugation[1], root, prefix, suffix, conjugation[3], conjugation[4]))

    return processed

# Download from https://kaikki.org/dictionary/Ancient%20Greek/kaikki.org-dictionary-AncientGreek.jsonl
df = pd.read_json(path_or_buf='data.jsonl', lines=True)

conjugations_list = []
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

for index, row in df.loc[df['pos'] == 'noun'].iterrows():
    if not isinstance(row['forms'], list):
        continue

    # Obtain definitions
    definitions = []
    for sense in row.senses:
        # No definition
        if sense.get('tags') and 'no-gloss' in sense['tags']:
            continue
        definitions += sense['glosses']

    if 'ἀεικείη' in row.word:
        print()

    conjugations = []
    declension = None

    # List of all conjugations for this word
    word_conjugations = []
    i = 0

    for form in row.forms:

        if 'table-tags' in form.get('tags'):
            # A new declension table starts here
            if conjugations:
                word_conjugations.append(process_conjugations(conjugations))
                i += 1

            conjugations = []
            declension = form['form']
            continue

        if 'inflection-template' in form.get('tags') or 'class' in form.get('tags'):
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
                print(f"Warning: invalid characters in word {word} of group {row.word}{i}")
                continue

            if word == "σι":
                print()

            conjugations.append((f"{row.word}{i}", declension, word, get_case(form['tags']), get_amount(form['tags'])))

    # End of the last conjugation
    if conjugations:
        word_conjugations.append(process_conjugations(conjugations))

    if word_conjugations:
        conjugations_list.append(word_conjugations)
        print(len(word_conjugations), len(row.inflection_templates))

pprint(conjugations_list, width=100)