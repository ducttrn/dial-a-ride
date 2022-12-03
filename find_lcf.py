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
            max_chain, max_chain_length = find_longest_chain_no_removals(graph_)
        else:
            max_chain, max_chain_length = find_longest_chain(graph_)

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
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data = {
        "1": ("B", "A"),
        "2": ("B", "G"),
        "3": ("B", "E"),
        "4": ("G", "C"),
        "5": ("B", "F"),
        "6": ("A", "D"),
        "7": ("E", "F"),
        "8": ("C", "D"),
        "9": ("G", "C"),
        "10": ("B", "F"),
        "11": ("A", "D"),
        "12": ("E", "H"),
        "13": ("C", "D"),
        "14": ("B", "G"),
        "15": ("H", "E"),
        "16": ("G", "H"),
        "17": ("B", "H"),
        "18": ("A", "B"),
        "19": ("G", "B"),
        "20": ("E", "B"),
        "21": ("C", "G"),
        "22": ("F", "B"),
        "23": ("D", "A"),
        "24": ("F", "E"),
        "25": ("D", "C"),
        "26": ("C", "G"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(f"LCF with Normal DFS: {find_lcf_outcome(graph, 27, no_removals=True)}")
    print(f"LCF with DFS-B: {find_lcf_outcome(graph, 27, no_removals=False)}")
