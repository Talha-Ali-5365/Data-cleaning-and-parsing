#!/usr/bin/env python3

import sys
import ast
from itertools import combinations

# Initialize itemset count dictionary
itemset_counts = {}

# Confidence threshold
confidence_threshold = 0.0

# Read input and aggregate counts
for line in sys.stdin:
    itemset, count = line.strip().split('\t')
    # Parse the itemset string back a tuple
    itemset = ast.literal_eval(itemset)
    count = int(count)
    itemset_counts[itemset] = itemset_counts.get(itemset, 0) + count

# Output counts for each itemset
for itemset, count in itemset_counts.items():
    print(f"{itemset}\tCount: {count}")

# Compute confidence scores and output rules
for itemset, itemset_count in itemset_counts.items():
    for n in range(1, len(itemset)):  # Change here to include n == len(itemset)
        for items in combinations(itemset, n):
            rule_lhs = items
            rule_rhs = tuple(item for item in itemset if item not in items)
            rule_lhs_count = itemset_counts[rule_lhs]
            confidence = itemset_count / rule_lhs_count
            if confidence >= confidence_threshold:
                print(f"{rule_lhs} -> {rule_rhs}\tConfidence: {confidence}")
