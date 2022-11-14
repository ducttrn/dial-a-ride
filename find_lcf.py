from find_lc import find_longest_chain
from find_opt import optimal
from graph import Graph, construct_graph


def find_lcf_outcome(graph: Graph, time_limit: int) -> int:
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0:
        max_chain, max_chain_length = find_longest_chain(graph)
        if jump_needed:
            time_remaining -= 1  # jump if not first request
        else:
            jump_needed = True

        if max_chain_length == 0 or time_remaining <= max_chain_length:
            served += time_remaining
            break

        served += max_chain_length
        time_remaining = time_remaining - max_chain_length
        for request_id in max_chain:
            graph.remove_request(request_id)

    return served


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "H"),
    }
    graph = construct_graph(node_ids_, request_data)
    print(f"Optimal: {optimal(graph, 7)}")
    print(f"LCF: {find_lcf_outcome(graph, 7)}")
