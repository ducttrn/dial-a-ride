from find_lcf import find_lcf_outcome
from find_opt import optimal2
from graph import generateRequestsUniform, Graph
from random import randrange
import time

if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G"]
    request_data = {
        "1": ("D", "B"),
        "2": ("E", "C"),
        "3": ("B", "C"),
        "4": ("F", "E"),
        "5": ("C", "E"),
        "6": ("B", "D"),
    }

    count = 0
    iterations = int(input("How many iterations do you want to run? "))
    time_limit_min = int(input("Minimum time limit? "))
    time_limit_max = int(input("Maximum time limit? "))
    nodes_min = int(input("Minimum number of nodes? "))
    nodes_max = int(input("Maximum number of nodes? "))
    requests_min = int(input("Minimum number of requests? "))
    requests_max = int(input("Maximum number of requests? "))
    print_to_terminal = int(input("Do you want to print the results to the terminal? 1 for yes and 0 for no: "))
    for i in range(iterations):
        start = time.time()
        time_limit = randrange(time_limit_min, time_limit_max)
        numberOfNodes = randrange(nodes_min, nodes_max)
        numberOfRequests = randrange(requests_min, requests_max)
        graph = generateRequestsUniform(numberOfNodes, numberOfRequests) # num of nodes needs to > 1

        opt = optimal2(graph, time_limit)
        lcf = find_lcf_outcome(graph, time_limit)
        ratio = float(opt/lcf)

        print(f"Iteration: {i+1}")
        
        if print_to_terminal:
            print(f"Number of nodes: {numberOfNodes}, Number of requests {numberOfRequests}")
            print(f"Graph Nodes: {[node for node in graph.nodes]}")
            print(f"Graph Requests: {[(request.id, request.src.id, request.dst.id) for request in graph.requests.values()]}")
            print(f"Time limit: {time_limit}")
            print(f"Optimal: {opt}")
            print(f"LCF: {lcf}")
            print(f"OPT to LCF ratio: {ratio}")
            print(f"Time taken: {time.time() - start}")
        print(f"Ratio greater than 1: {count} times")
        print(f"---------------------------")
        if ratio < 1:
            f = open("wrong_ratio.txt", "a")
            f.write(f"Number of nodes: {numberOfNodes}, Number of requests {numberOfRequests}")
            f.write(f"Graph Nodes: {[node for node in graph.nodes]}")
            f.write(f"Graph Requests: {[(request.id, request.src.id, request.dst.id) for request in graph.requests.values()]}")
            f.write(f"Time limit: {time_limit}")
            f.write(f"Optimal: {opt}")
            f.write(f"LCF: {lcf}")
            f.write(f"OPT to LCF ratio: {ratio}")
            f.write(f"---------------------------")
            f.close()
            raise Exception(f"Wrong ratio")
        elif ratio > 1:
            count += 1
            f = open("ratio.txt", "a")
            f.write(f"Number of nodes: {numberOfNodes}, Number of requests {numberOfRequests}")
            f.write(f"Graph Nodes: {[node for node in graph.nodes]}")
            f.write(f"Graph Requests: {[(request.id, request.src.id, request.dst.id) for request in graph.requests.values()]}")
            f.write(f"Time limit: {time_limit}")
            f.write(f"Optimal: {opt}")
            f.write(f"LCF: {lcf}")
            f.write(f"OPT to LCF ratio: {ratio}")
            f.write(f"---------------------------")
            f.close()
