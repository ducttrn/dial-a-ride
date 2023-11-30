from typing import Dict
import secrets


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
    """
    Class to represent a graph
    """
    def __init__(self, nodes: Dict[str, Node], requests: Dict[str, Request]):
        self.nodes = nodes
        self.requests = requests

    def remove_request(self, request_id: str):
        request = self.requests[request_id]
        request.src.out_requests.remove(request_id)
        request.dst.in_requests.remove(request_id)
        del self.requests[request_id]


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


def generate_requests_uniform(nodes_count: int, requests_count: int) -> Graph:
    # number of nodes is less than 26
    node_ids_ = [chr(node + 65) for node in range(nodes_count)]
    request_data = {}

    for i in range(requests_count):
        source = secrets.SystemRandom().randrange(nodes_count)
        destination = secrets.SystemRandom().randrange(nodes_count)
        while destination == source:
            destination = secrets.SystemRandom().randrange(nodes_count)

        request_data[str(i + 1)] = (node_ids_[source], node_ids_[destination])

    graph = construct_graph(node_ids_, request_data)
    return graph
