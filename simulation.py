import time
from random import randrange
from typing import TextIO

from find_lcf import find_lcf_outcome
from find_opt import find_optimal
from graph import generate_requests_uniform, Graph


def write_instance_to_file(file: TextIO, graph: Graph, time_limit: int, opt: int, lcf: int):
    nodes = [node for node in graph.nodes]
    requests = [(request.id, request.src.id, request.dst.id) for request in graph.requests.values()]

    file.write(f"Number of nodes: {len(nodes)}, Number of requests {len(requests)}\n")
    file.write(f"Graph Nodes: {nodes}\n")
    file.write(f"Graph Requests: {requests}\n")
    file.write(f"Time limit: {time_limit}\n")
    file.write(f"Optimal: {opt}\n")
    file.write(f"LCF: {lcf}\n")
    file.write(f"OPT to LCF ratio: {float(opt / lcf)}\n")
    file.write(f"---------------------------\n")


if __name__ == "__main__":
    iterations = int(input("How many iterations do you want to run? "))
    time_limit_min = int(input("Minimum time limit? "))
    time_limit_max = int(input("Maximum time limit? "))
    nodes_min = int(input("Minimum number of nodes? "))
    nodes_max = int(input("Maximum number of nodes? "))
    requests_min = int(input("Minimum number of requests? "))
    requests_max = int(input("Maximum number of requests? "))
    print_to_terminal = int(input("Do you want to print the results to the terminal? 1 for yes and 0 for no: "))

    greater_than_one = 0
    for i in range(iterations):
        start = time.time()
        time_limit = randrange(time_limit_min, time_limit_max + 1)
        nodes_count = randrange(nodes_min, nodes_max + 1)
        requests_count = randrange(requests_min, requests_max + 1)
        graph = generate_requests_uniform(nodes_count, requests_count)  # num of nodes needs to > 1

        opt = find_optimal(graph, time_limit)
        lcf = find_lcf_outcome(graph, time_limit, no_removals=True)
        ratio = float(opt / lcf)

        print(f"Iteration: {i + 1}")

        if print_to_terminal:
            print(f"Number of nodes: {nodes_count}, Number of requests {requests_count}")
            print(f"Graph Nodes: {[node for node in graph.nodes]}")
            print(f"Graph Requests: {[(rq.id, rq.src.id, rq.dst.id) for rq in graph.requests.values()]}")
            print(f"Time limit: {time_limit}")
            print(f"Optimal: {opt}")
            print(f"LCF: {lcf}")
            print(f"OPT to LCF ratio: {ratio}")
            print(f"Time taken: {time.time() - start}")
            print(f"Ratio greater than 1: {greater_than_one} times")
            print(f"---------------------------")

        if ratio < 1:
            with open("wrong_ratios.txt", "a") as f:
                write_instance_to_file(f, graph, time_limit, opt, lcf)
            raise Exception(f"Wrong ratio -- see wrong_ratios.txt for details")

        elif ratio > 1:
            greater_than_one += 1
            with open("ratios.txt", "a") as f:
                write_instance_to_file(f, graph, time_limit, opt, lcf)
