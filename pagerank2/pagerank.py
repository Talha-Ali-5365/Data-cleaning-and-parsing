import numpy as np
from subprocess import check_output

# Number of nodes
N = 6

# Initialize PageRank vector (assuming equal initial ranks)
pagerank = np.ones(N) / N

# Read the transition matrix from the output of the MapReduce job
transition_matrix = np.zeros((N, N))
output = check_output(["hadoop", "fs", "-cat", "/inputs/output3/part-00000"]).decode().strip().split("\n")
for line in output:
    row, values = line.split("\t")
    row_idx = int(row)
    if row_idx >= N:
        continue
    values = list(map(float, values.split(",")))
    # Pad the values list with zeros to match the number of nodes
    values.extend([0.0] * (N - len(values)))
    transition_matrix[row_idx] = values

# Perform matrix multiplication for at least 10 iterations
for iteration in range(10):
    pagerank = np.dot(transition_matrix, pagerank)
    print(f"Iteration {iteration + 1}: {pagerank}")
