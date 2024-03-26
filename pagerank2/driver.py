#!/usr/bin/env python3

import sys
import subprocess

# Set maximum number of iterations
MAX_ITERATIONS = 1

def run_mapreduce_job(input_path, output_path, mapper_path, reducer_path):
    # Run the MapReduce job
    cmd = [
        "hadoop",
        "jar",
        "/usr/local/hadoop-2.10.2/share/hadoop/tools/lib/hadoop-streaming-2.10.2.jar",
        "-input",
        input_path,
        "-output",
        output_path,
        "-mapper",
        "mapper.py",
        "-reducer",
        "reducer.py",
        "-file",
        mapper_path,
        "-file",
        reducer_path
    ]
    subprocess.run(cmd)

def initialize_pageranks(input_path, output_path):
    # Copy input to output to start the first iteration
    subprocess.run(["hadoop", "fs", "-cp", input_path, output_path])


def main(input_path, output_path, mapper_path, reducer_path):
    # Initialize PageRank values for the first iteration
    initialize_pageranks(input_path, output_path)
    
    # Iterate until convergence or maximum iterations reached
    for i in range(MAX_ITERATIONS):
        # Run MapReduce job
        if(i==0):
            run_mapreduce_job(output_path, output_path + f"_iter_{i}", mapper_path, reducer_path)
        else:
            run_mapreduce_job(output_path+ f"_iter_{i-1}", output_path + f"_iter_{i}", mapper_path, reducer_path)
        
        

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: pagerank_driver.py <input_path> <output_path> <mapper_path> <reducer_path> <iterations>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    mapper_path = sys.argv[3]
    reducer_path = sys.argv[4]
    MAX_ITERATIONS = int(sys.argv[5])
    main(input_path, output_path, mapper_path, reducer_path)

