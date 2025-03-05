import pandas as pd

from data.scraping.noun_metadata import get_metadata
from data.scraping.scrape_wiktionary import int_from_amount, int_from_case, int_from_gender

file = 'data/raw/ancient_greek_first-declension_nouns'

df = pd.read_csv(file + '_parsed.csv', header=None)

conjugations_list = []
roots_list = []

with open(file + '_grouped.txt') as f:
    for line in f:
        group = line.split()[0]

        conjugations = df.loc[df[0] == group]

        for c in conjugations.fillna('').values.tolist():
            # conjugation_group, prefix, prefix_without_accents, suffix, suffix_without_accents, morphological_amount, morphological_case
            conjugations_list.append(f"('{group}', '{c[3]}', '{c[4]}', '{c[5]}', '{c[6]}', {int_from_amount(c[11])}, {int_from_case(c[10])})")

        for nominative_singular in line.split():
            c = df.loc[df[0] == nominative_singular].fillna('').values.tolist()[0]
            # root, root_without_accents, conjugation_group, gender, exact, metadata
            roots_list.append(f"('{c[1]}', '{c[2]}', '{group}', {int_from_gender(c[9])}, '{c[12]}')")

            if int_from_gender(c[9]) == -1:
                print(c[9])

with open(file + '.sql', 'w') as f:

    f.write("INSERT INTO noun_conjugation_table (conjugation_group, prefix, prefix_without_accents, suffix, suffix_without_accents, morphological_amount, morphological_case) VALUES\n")
    for i, conjugation in enumerate(conjugations_list):
        if i == len(conjugations_list) - 1:
            f.write(conjugation + ';\n')
        else:
            f.write(conjugation + ',\n')

    f.write("\nINSERT INTO noun_roots_table (root, root_without_accents, conjugation_group, gender, metadata) VALUES\n")
    for i, root in enumerate(roots_list):
        if i == len(roots_list) - 1:
            f.write(root + ';\n')
        else:
            f.write(root + ',\n')