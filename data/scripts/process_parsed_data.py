import sys
from typing import Tuple

import pandas as pd


def get_grouped(df):
    grouped = df.groupby(0)

    unique_groups = {}

    for name, group in grouped:
        important_values = group[[2, 3, 5, 6, 7]].fillna('NULL').values.tolist()

        key = tuple(map(tuple, important_values))

        if key not in unique_groups:
            unique_groups[key] = []

        unique_groups[key].append(group.values[0][0])

    return unique_groups.values()


def int_from_amount(amount_str: str) -> int:
    amounts = {
        "Singular": 0,
        "Dual": 1,
        "Plural": 2
    }
    return amounts.get(amount_str)

def int_from_case(case_str: str) -> int:
    cases = {
        "Nominative": 0,
        "Genitive": 1,
        "Dative": 2,
        "Accusative": 3,
        "Vocative": 4
    }
    return cases.get(case_str)

def int_from_gender(gender_str: Tuple[str] | str) -> int:
    genders = {
        "Masculine": 0,
        "Feminine": 1,
        "MasculineOrFeminine": 2,
        "Neuter": 3
    }
    return genders.get(str(gender_str))

def format(df, group):
    conjugations_list = []
    roots_list = []

    conjugations = df.loc[df[0] == group[0]]

    for c in conjugations.fillna('').values.tolist():
        # conjugation_group, prefix, suffix, morphological_amount, morphological_case
        conjugations_list.append(f"('{group[0]}', '{c[2]}', '{c[3]}', {int_from_amount(c[7])}, {int_from_case(c[6])})")

    for id in group:
        c = df.loc[df[0] == id].fillna('').values.tolist()[0]
        # root, conjugation_group, gender, metadata
        roots_list.append(f"('{c[1]}', '{group[0]}', {int_from_gender(c[5])}, '{c[8]}')")

        if int_from_gender(c[5]) == -1:
            print(c[0], c[5])

    return conjugations_list, roots_list

def main(folder):
    df = pd.read_csv(folder + 'parsed.csv', header=None)

    print("Grouping data")

    groups = get_grouped(df)

    with open(folder + 'grouped.txt', mode='w', newline='') as f:
        for group in groups:
            for entry in group:
                f.write(entry + " ")
            f.write("\n")

    conjugations = []
    roots = []

    for i, group in enumerate(groups):
        print(f"\rProcessing group {i}/{len(groups)}", end='')
        formatted = format(df, group)
        conjugations += formatted[0]
        roots += formatted[1]

    print("Finished processing.")

    with open(folder + 'processed.sql', 'w') as f:
        f.write("INSERT INTO noun_conjugation_table (conjugation_group, prefix, suffix, morphological_amount, morphological_case) VALUES\n")
        for i, conjugation in enumerate(conjugations):
            if i == len(conjugations) - 1:
                f.write(conjugation + ';\n')
            else:
                f.write(conjugation + ',\n')

        f.write("\nINSERT INTO noun_roots_table (root, conjugation_group, gender, metadata) VALUES\n")
        for i, root in enumerate(roots):
            if i == len(roots) - 1:
                f.write(root + ';\n')
            else:
                f.write(root + ',\n')

if __name__ == '__main__':
    main(sys.argv[1])
