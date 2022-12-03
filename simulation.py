import csv
from random import randrange

from find_lcf import find_lcf_outcome
from graph import generate_requests_uniform


def write_instance_to_file(
        iteration: int,
        requests_count: int,
        nodes_count: int,
        time_limit: int,
        dfs_backtrack: int,
        dfs_normal: int
    ):
    data = [
        iteration,
        requests_count,
        nodes_count,
        time_limit,
        dfs_backtrack,
        dfs_normal,
        float(dfs_backtrack / dfs_normal)
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
        time_limit = randrange(time_limit_min, time_limit_max + 1)
        nodes_count = randrange(nodes_min, nodes_max + 1)
        requests_count = randrange(requests_min, requests_max + 1)
        graph = generate_requests_uniform(nodes_count, requests_count)  # num of nodes needs to > 1

        dfs_normal = find_lcf_outcome(graph, time_limit, no_removals=True)
        dfs_backtrack = find_lcf_outcome(graph, time_limit, no_removals=False)
        write_instance_to_file(i + 1, requests_count, nodes_count, time_limit, dfs_backtrack, dfs_normal)