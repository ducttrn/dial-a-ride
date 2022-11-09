import itertools
import time

from graph import construct_graph


def calculate_served_requests(graph, permutation, time_limit) -> int:
    requests_served = 0
    time_left = time_limit
    current_destination = graph.requests[permutation[0]].src.id
    request_index = 0

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

    print(permutation, requests_served)
    return requests_served, last_request


def optimal(graph, time_limit) -> int:
    start = time.time()
    max_requests = 0  # maximum number of requests served within time limit
    requests = graph.requests
    permutations = list(itertools.permutations(requests, len(requests)))  # list of request IDs
    current_request = 0
    last_request = 0

    for perm in permutations:
        if perm[last_request] != current_request:
            requests_served, last_request = calculate_served_requests(graph, perm, time_limit)
            max_requests = max(max_requests, requests_served)
            current_request = last_request

    print(f"Time taken: {time.time() - start}")
    return max_requests


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "F"),
        "8": ("G", "H"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(optimal(graph, 7))

    request_data = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "F"),
        "8": ("F", "G"),
        "9": ("G", "F"),
        "10": ("G", "H"),
        "11": ("G", "C"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(optimal(graph, 10))
