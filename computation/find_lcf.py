import copy

from find_lc import find_longest_chain, find_longest_chain_no_removals
from graph import Graph, construct_graph


def find_lcf_outcome(graph: Graph, time_limit: int, no_removals=False) -> int:
    graph_ = copy.deepcopy(graph)  # deepcopy to avoid removing edges from the original graph
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0:
        if no_removals:
            max_chain = find_longest_chain_no_removals(graph_)
        else:
            max_chain = find_longest_chain(graph_)

        max_chain_length = len(max_chain)
        if max_chain_length == 0:
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
        "11": ("A", "D"),
        "12": ("A", "D"),
        "13": ("C", "B"),
        "14": ("A", "D"),
        "15": ("C", "D"),
        "16": ("D", "A"),
        "17": ("A", "B"),
        "18": ("A", "D"),
        "19": ("A", "C"),
        "20": ("B", "A"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(f"LCF with Normal DFS: {find_lcf_outcome(graph, 28, no_removals=True)}")
    print(f"LCF with DFS-B: {find_lcf_outcome(graph, 28, no_removals=False)}")
