#!/usr/bin/env python3

import sys

def mapper():
    # Input comes from STDIN
    for line in sys.stdin:
        # Parse the input from file
        node_id, pagerank, neighbors = line.strip().split('\t')
        pagerank = float(pagerank)
        neighbors = neighbors.strip().split(',')

        # Emit key-value pairs for the transition matrix
        for neighbor in neighbors:
            print(f"{neighbor}\t{node_id}:{pagerank / len(neighbors)}")

if __name__ == "__main__":
    mapper()