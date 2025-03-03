import pandas as pd

df = pd.read_csv('data/raw/ancient_greek_first-declension_nouns.txt_parsed.csv', header=None)
grouped = df.groupby(0)

unique_groups = {}

for name, group in grouped:
    important_values = group[[3, 5, 9, 10, 11]].fillna('NULL').values.tolist()

    key = tuple(map(tuple, important_values))

    if key not in unique_groups:
        unique_groups[key] = []

    unique_groups[key].append(group.values.tolist())

result = [groups for groups in unique_groups.values() if len(groups) > 1]

for idx, group in enumerate(result):
    print(f"\nGroup {idx + 1}:")
    for entry in group:
        print(entry[0][0], end=" ")
