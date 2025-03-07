import pandas as pd

file = 'data/raw/ancient_greek_third-declension_nouns_parsed.csv'

df = pd.read_csv(file, header=None)
grouped = df.groupby(0)

unique_groups = {}

for name, group in grouped:
    important_values = group[[2, 3, 5, 6, 7]].fillna('NULL').values.tolist()

    key = tuple(map(tuple, important_values))

    if key not in unique_groups:
        unique_groups[key] = []

    unique_groups[key].append(group.values.tolist())

result = [groups for groups in unique_groups.values() if len(groups) > 1]

with open(file.replace('parsed.csv', 'grouped.txt'), mode='w', newline='') as f:
    for idx, group in enumerate(result):
        for entry in group:
            f.write(entry[0][0] + " ")
        f.write("\n")