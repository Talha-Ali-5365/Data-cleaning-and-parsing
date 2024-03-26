#!/usr/bin/env python3

import sys

def reducer():
    current_node = None
    transition_values = []

    # Input comes from STDIN
    for line in sys.stdin:
        # Parse the input from mapper
        node_id, transition_value = line.strip().split('\t')
        transition_value = float(transition_value.split(':')[1])

        if current_node is None:
            current_node = node_id

        if current_node != node_id:
            # Emit the accumulated transition values for the previous node
            print(f"{current_node}\t{','.join(map(str, transition_values))}")
            current_node = node_id
            transition_values = []

        transition_values.append(transition_value)

    # Emit the accumulated transition values for the last node
    print(f"{current_node}\t{','.join(map(str, transition_values))}")

if __name__ == "__main__":
    reducer()