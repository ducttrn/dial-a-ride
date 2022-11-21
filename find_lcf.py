from find_lc import find_longest_chain, find_longest_chain_no_removals
from find_opt import optimal2
from graph import construct_graph, generateRequestsUniform, Graph
from random import randrange


def find_lcf_outcome(graph: Graph, time_limit: int, no_removals=False) -> int:
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0:
        if no_removals:
            max_chain, max_chain_length = find_longest_chain_no_removals(graph)
        else:
            max_chain, max_chain_length = find_longest_chain(graph)

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
            graph.remove_request(request_id)

    return served


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

    for i in range(5):
        time_limit = randrange(1,15)
        graph = generateRequestsUniform(numberOfNodes = randrange(2,7), numberOfRequests = randrange(5,8)) # num of nodes needs to > 1

        opt = optimal2(graph, time_limit)
        lcf = find_lcf_outcome(graph, time_limit)

        print(f"Iteration: {i+1}")
        print(f"Time limit: {time_limit}")
        print(f"Optimal: {opt}")
        print(f"LCF: {lcf}")

        print(f"OPT to LCF ratio: {float(opt/lcf)}")
