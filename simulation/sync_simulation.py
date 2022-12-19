import csv
from random import randrange
from typing import Optional

from computation.find_lcf import find_lcf_outcome
from graph import generate_requests_uniform


def write_instance_to_file(
        requests_count: int,
        nodes_count: int,
        time_limit: int,
        lcf: int,
        dfs: int,
        optimal: Optional[int],
) -> None:
    data = [
        requests_count,
        nodes_count,
        time_limit,
        lcf,
        dfs,
        optimal,
    ]
    with open('simulation-data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


if __name__ == "__main__":
    iterations = int(input("How many iterations do you want to run? "))
    time_limit_min = int(input("Minimum time limit? "))
    time_limit_max = int(input("Maximum time limit? "))
    nodes_min = int(input("Minimum number of nodes? "))
    nodes_max = int(input("Maximum number of nodes? "))
    requests_min = int(input("Minimum number of requests? "))
    requests_max = int(input("Maximum number of requests? "))

    for i in range(iterations):
        print(f"Iteration: {i + 1}")
        nodes_count = randrange(nodes_min, nodes_max + 1)
        requests_count = randrange(requests_min, requests_max + 1)
        # num of nodes needs to > 1
        # pick relatively big number of nodes to avoid long runtime of DFS-B
        scaled_nodes_count = max(nodes_count, requests_count // 3)
        print(f"Nodes: {scaled_nodes_count}, Requests: {requests_count}, Time: {15}")

        graph = generate_requests_uniform(scaled_nodes_count, requests_count)
        dfs = find_lcf_outcome(graph, 15, no_removals=True)
        lcf = find_lcf_outcome(graph, 15, no_removals=False)
        write_instance_to_file(requests_count, scaled_nodes_count, 15, lcf, dfs, None)
