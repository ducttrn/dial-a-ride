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
    time_limit_min = 75
    time_limit_max = 76
    nodes_min = 50
    nodes_max = 51
    requests_min = 100
    requests_max = 101

    total = 0
    for i in range(200):
        print(f"Iteration: {i + 1}")
        nodes_count = randrange(nodes_min, nodes_max)
        requests_count = randrange(requests_min, requests_max)
        time_limit = randrange(time_limit_min, time_limit_max)

        print(f"Nodes: {nodes_count}, Requests: {requests_count}, Time: {15}")

        graph = generate_requests_uniform(nodes_count, requests_count)
        dfs = find_lcf_outcome(graph, time_limit, no_removals=True)
        total += dfs
    print(f"DFS: {total / 200}")
