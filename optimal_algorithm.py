import itertools

from typing import Dict


class Node:
    def __init__(self, _id: str):
        self.id = _id
        self.in_requests = set()
        self.out_requests = set()


class Request:
    def __init__(self, _id: str, src: Node, dst: Node):
        self.id = _id
        self.src = src
        self.dst = dst


class Graph:
    def __init__(self, nodes: Dict[str, Node], requests: Dict[str, Request]):
        self.nodes = nodes
        self.requests = requests


def construct_graph(node_ids, request_data) -> Graph:
    nodes = {node_id: Node(node_id) for node_id in node_ids}

    for request_id, (src_id, dst_id) in request_data.items():
        nodes[src_id].out_requests.add(request_id)
        nodes[dst_id].in_requests.add(request_id)

    requests = {}
    for request_id, (src_id, dst_id) in request_data.items():
        request = Request(request_id, nodes[src_id], nodes[dst_id])
        requests[request_id] = request

    graph = Graph(nodes, requests)
    return graph


def calculate_served_requests(graph, permutation, time_limit) -> int:
    requests_served = 0
    time_left = time_limit
    current_destination = graph.requests[permutation[0]].src.id
    request_index = 0

    while time_left > 0:
        request_ID = permutation[request_index]
        request = graph.requests[request_ID]
        
        if current_destination == request.src.id:
            requests_served += 1
            time_left -= 1
            current_destination = request.dst.id
            request_index += 1
        else:
            time_left -= 1
            current_destination = request.src.id

    print(permutation, requests_served)
    return requests_served


def optimal(graph, time_limit) -> int:

    max_requests = 0 # maximum number of requests served within time limit
    #permutations = itertools.permutations
    
    nodes = graph.nodes
    requests = graph.requests
    permutations = list(itertools.permutations(requests, len(requests))) # list of request IDs

    for perm in permutations:
        max_requests = max(max_requests, calculate_served_requests(graph, perm, time_limit))

    return max_requests


def main():
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data_ = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "F"),
        "8": ("G", "H"),
    }
    graph = construct_graph(node_ids_, request_data_)
    
    print(optimal(graph, 7))


main()
