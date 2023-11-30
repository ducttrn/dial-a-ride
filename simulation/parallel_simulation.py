
from joblib import Parallel, delayed

from computation.find_lcf import find_lcf_outcome
from graph import generate_requests_uniform
from simulation.sync_simulation import write_instance_to_file
import secrets


# Run simulations in parallel to save time
# good for running exponential algorithms but unnecessary for polynomial ones
def process(i, time_limit_min, time_limit_max, nodes_min, nodes_max, requests_min, requests_max, seed):
    # Seed to avoid generating the same graph for each process
    # https://stackoverflow.com/questions/31740561/random-number-generator-using-joblib
    print(f"Iteration: {i + 1}")

    secrets.SystemRandom().seed(seed)
    time_limit = secrets.SystemRandom().randrange(time_limit_min, time_limit_max + 1)
    nodes_count = secrets.SystemRandom().randrange(nodes_min, nodes_max + 1)
    requests_count = secrets.SystemRandom().randrange(requests_min, requests_max + 1)

    # avoid giving too much time to see the difference between lcf and dfs
    scaled_time_limit = min(time_limit, requests_count * 2 - 1)
    # num of nodes needs to > 1
    # pick relatively big number of nodes to avoid long runtime of DFS-B
    scaled_nodes_count = max(nodes_count, requests_count // 3)

    graph = generate_requests_uniform(scaled_nodes_count, requests_count)
    lcf = find_lcf_outcome(graph, scaled_time_limit, no_removals=True)
    dfs = find_lcf_outcome(graph, scaled_time_limit, no_removals=False)
    write_instance_to_file(i + 1, requests_count, scaled_nodes_count, scaled_time_limit, lcf, dfs)


if __name__ == "__main__":
    iterations = int(input("How many iterations do you want to run? "))
    time_limit_min = int(input("Minimum time limit? "))
    time_limit_max = int(input("Maximum time limit? "))
    nodes_min = int(input("Minimum number of nodes? "))
    nodes_max = int(input("Maximum number of nodes? "))
    requests_min = int(input("Minimum number of requests? "))
    requests_max = int(input("Maximum number of requests? "))

    # Joblib doc: n_jobs=-1 means using processors
    results = Parallel(n_jobs=-1)(
        delayed(process)(
            i, time_limit_min, time_limit_max, nodes_min, nodes_max, requests_min, requests_max, secrets.SystemRandom().randrange(1, 100)
        ) for i in range(iterations)
    )
