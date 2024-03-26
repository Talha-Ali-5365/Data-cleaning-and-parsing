#!/usr/bin/env python3

import sys
import itertools

def generate_subsets(items):
    subsets = []
    for n in range(1, len(items) + 1):
        subsets.extend(itertools.combinations(items, n))
    return subsets

min_support = 1

# Initialize itemset count dictionary
itemset_counts = {}

# Read input and count occurrences of each itemset
for line in sys.stdin:
    items = line.strip().split()
    itemsets = generate_subsets(items)
    for itemset in itemsets:
        itemset_counts[itemset] = itemset_counts.get(itemset, 0) + 1

# Output frequent itemsets above minimum support threshold
for itemset, count in itemset_counts.items():
    if count >= min_support:
        print(f"{itemset}\t{count}")