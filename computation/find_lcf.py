import copy

from .find_lc import find_longest_chain, find_longest_chain_no_removals
from graph import Graph, construct_graph


def find_lcf_outcome(graph: Graph, time_limit: int, no_removals=False) -> int:
    """
    Find the outcome of the LCF algorithm on a given graph and time limit.
    :param graph
    :param time_limit
    :param no_removals: if True, use the LCF algorithm with no removals (DFS as described in the paper)
    :return:
    """
    graph_ = copy.deepcopy(graph)  # deepcopy to avoid removing edges from the original graph
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0:
        if no_removals:
            max_chain = find_longest_chain_no_removals(graph_)
        else:
            max_chain = find_longest_chain(graph_)

        if (max_chain_length := len(max_chain)) == 0:
            return served

        if jump_needed:
            time_remaining -= 1  # jump if not first request
        else:
            jump_needed = True

        if time_remaining <= max_chain_length:
            served += time_remaining
            return served

        served += max_chain_length
        time_remaining = time_remaining - max_chain_length
        for request_id in max_chain:
            graph_.remove_request(request_id)  # directly remove served requests from graph

    return served


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D"]
    request_data = {
        "1": ("D", "A"),
        "2": ("D", "C"),
        "3": ("B", "D"),
        "4": ("A", "D"),
        "5": ("C", "A"),
        "6": ("A", "B"),
        "7": ("D", "A"),
        "8": ("B", "D"),
        "9": ("A", "C"),
        "10": ("A", "C"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(f"LCF with Normal DFS: {find_lcf_outcome(graph, 28, no_removals=True)}")
    print(f"LCF with DFS-B: {find_lcf_outcome(graph, 28, no_removals=False)}")
