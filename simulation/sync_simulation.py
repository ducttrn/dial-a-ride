import csv
import time
from collections import Counter
from typing import Optional

from computation.find_lcf import find_lcf_outcome
from computation.find_k_chain import find_k_chain_outcome
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


def simulate_lcf_using_k_chain():
    """
    Simulate LCF using k-chain algorithm by calling 30-chain on graphs known to have no chains longer than 25.
    This method is polynomial time, compared to exponential time of LCF.
    """
    time_limit = 100
    nodes_count = 50

    for requests_count in [25, 50, 75, 100]:
        lcf = 0
        one = 0
        two = 0
        three = 0
        four = 0
        dfs = 0
        non_k_count = 0
        while non_k_count < 200:
            graph = generate_requests_uniform(nodes_count, requests_count)
            alg, chains_k_ = find_k_chain_outcome(graph, time_limit, 30)
            if not chains_k_:
                lcf += alg
                non_k_count += 1
                dfs += find_lcf_outcome(graph, time_limit, True)
                for j in range(1, 5):
                    alg, _ = find_k_chain_outcome(graph, time_limit, j)
                    if j == 1:
                        one += alg
                    elif j == 2:
                        two += alg
                    elif j == 3:
                        three += alg
                    elif j == 4:
                        four += alg
        print(f"{one / non_k_count}")
        print(f"{two / non_k_count}")
        print(f"{three / non_k_count}")
        print(f"{four / non_k_count}")
        print(f"{lcf / non_k_count}")
        print(f"{dfs / non_k_count}")
        print("------------------")


def simulate_k_chain(nodes_count, requests_count, time_limit):
    """
    Simulate k-chain algorithms (k from 1 to 25) by calling them on the 200 generated graphs and averaging the results.
    """
    for k in range(1, 25):
        total = 0
        chains = {}
        for i in range(200):
            graph = generate_requests_uniform(nodes_count, requests_count)
            alg, chains_k_, chains_ = find_k_chain_outcome(graph, time_limit, k)
            total += alg
            chains = dict(Counter(chains) + Counter(chains_))
        chains = {k: v / 200 for k, v in sorted(chains.items())}
        print(chains)
        print("------------------")


def simulate_dfs(nodes_count, requests_count, time_limit):
    """
    Simulate DFS on 200 generated graphs and average the results.
    Set the flag in find_lcf_outcome to True to simulate DFS.
    """
    total = 0
    for i in range(200):
        graph = generate_requests_uniform(nodes_count, requests_count)
        alg = find_lcf_outcome(graph, time_limit, True)
        total += alg
    print(f"{total / 200}")


def compare_k_chain_time_performance(nodes_count, requests_count, time_limit):
    """
    Compare the time performance of k-chain algorithms (k from 1 to 25) by calling them on the 200 generated graphs
    While measuring the runtime/
    """
    total_perf = [0] * 25  # 25 because running 25 k-chain algorithms (1 to 25), can be changed for other settings
    total_time = [0] * 25
    for i in range(200):
        graph = generate_requests_uniform(nodes_count, requests_count)
        for j in range(1, 26):
            t0 = time.time()
            alg, chains = find_k_chain_outcome(graph, time_limit, j)
            total_time[j - 1] += time.time() - t0
            total_perf[j - 1] += alg

    for x in total_perf:
        print(x / 200)
    for y in total_time:
        print(y / 200)
