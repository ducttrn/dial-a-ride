from typing import List
import numpy as np
from sympy.utilities.iterables import multiset_permutations

from graph import construct_graph, Graph


def calculate_served_requests(graph: Graph, permutation: List[str], time_limit: int) -> (int, int):
    requests_served = 0
    time_left = time_limit
    current_destination = graph.requests[permutation[0]].src.id
    request_index = 0
    last_request = 0

    while time_left > 0 and request_index < len(permutation):
        request_id = permutation[request_index]
        request = graph.requests[request_id]
        last_request = request_index

        if current_destination == request.src.id:
            requests_served += 1
            time_left -= 1
            current_destination = request.dst.id
            request_index += 1
        else:
            time_left -= 1
            current_destination = request.src.id

    return requests_served, permutation[:last_request+1]


def find_optimal(graph: Graph, time_limit: int) -> int:
    if time_limit > 2 * len(graph.requests.keys()):
        return len(graph.requests.keys())

    max_requests = 0  # maximum number of requests served within time limit
    requests = graph.requests
    array = np.array(list(requests.keys()))
    if time_limit < len(graph.requests.keys()):
        permutations = multiset_permutations(array, size=time_limit)  # find a way to do lazy loading/save memory
    else:
        permutations = multiset_permutations(array)  # list of request IDs

    last_perm = [0]

    for perm in permutations:
        if perm[:len(last_perm)] != last_perm:
            requests_served, current_perm = calculate_served_requests(graph, perm, time_limit)
            max_requests = max(max_requests, requests_served)
            last_perm = current_perm

    return max_requests


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data = {
        "1": ("E", "H"),
        "2": ("H", "D"),
        "3": ("D", "E"),
        "4": ("D", "B"),
        "5": ("A", "D"),
        "6": ("A", "C"),
        "7": ("B", "A"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(f"Optimal: {find_optimal(graph, 7)}")
