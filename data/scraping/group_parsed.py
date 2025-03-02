import csv
from collections import defaultdict

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0

# Initialize a defaultdict to store the data
data_dict = defaultdict(dict)

# Read the CSV data
with open('data/raw/ancient_greek_first-declension_nouns.txt_parsed.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        outer_key = row[0]
        inner_key = (row[-2], row[-3], row[-4])
        inner_value = row[1:-3]
        data_dict[outer_key][inner_key] = inner_value

# Create a union-find instance
uf = UnionFind()

# Map to keep track of the indices of each row
index_map = {}

# Populate the union-find structure
for index, (outer_key, inner_dict) in enumerate(data_dict.items()):
    for inner_key in inner_dict.keys():
        uf.add(index)  # Add the index to the union-find structure
        index_map[index] = outer_key  # Map index to outer key
        # Union the current index with others that share the same inner_key
        for other_index in index_map:
            if other_index != index and inner_key in data_dict[index_map[other_index]]:
                uf.union(index, other_index)

# Collect the results
groups = defaultdict(list)
for index in range(len(data_dict)):
    root = uf.find(index)
    groups[root].append(index_map[index])

# Convert the groups to a list of lists
result = list(groups.values())

# Print the resulting groups
for group in result:
    print(group)
