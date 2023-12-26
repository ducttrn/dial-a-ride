import copy

from graph import Graph, construct_graph


def find_k_chain_outcome(graph: Graph, time_limit: int, k: int):
    """
    Find the number of requests served by the k-chain algorithm
    """
    graph_ = copy.deepcopy(graph)  # deepcopy to avoid removing edges from the original graph
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False
    original_k = k
    chains_length_k = 0 # keep track of the number of chains of length k in the graph

    while time_remaining > 0 and len(graph_.requests):
        chain_to_serve = None
        while not chain_to_serve and k > 0:
            chain_to_serve = find_chain_k(graph_, k)
            if not chain_to_serve:
                k -= 1

        if len(chain_to_serve) == original_k:
            chains_length_k += 1

        if jump_needed:
            time_remaining -= 1
        else:
            jump_needed = True

        if time_remaining <= len(chain_to_serve):
            served += time_remaining
            return served, chains_length_k
        else:
            served += len(chain_to_serve)
            time_remaining -= len(chain_to_serve)
            chain_endpoint = graph_.requests[chain_to_serve[-1]].dst
            for request_id in chain_to_serve:
                graph_.remove_request(request_id)
            while time_remaining > 0 and len(graph_.requests) and chain_endpoint.out_requests:
                request_id = list(chain_endpoint.out_requests)[0]
                chain_endpoint = graph_.requests[request_id].dst
                graph_.remove_request(request_id)
                served += 1
                time_remaining -= 1

    return served, chains_length_k


def find_chain_k(graph: Graph, k: int):
    """
    Find any chain of length k
    """

    def find_chain_k_(k: int, current_chain: list[str]):
        last_request = graph.requests[current_chain[-1]]
        if k == 0:
            return current_chain

        if k == 1:
            for request_id in last_request.dst.out_requests:
                if request_id not in current_chain:
                    return current_chain + [request_id]
            return []

        for request_id in last_request.dst.out_requests:
            if request_id not in current_chain:
                chain = find_chain_k_(k - 1, current_chain + [request_id])
                if chain:
                    return chain

        return []

    for request in graph.requests.values():
        if chain := find_chain_k_(k - 1, [request.id]):
            return chain

    return []


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    request_data = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("A", "D"),
        "4": ("D", "E"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "H"),
        "8": ("H", "I"),
    }
    graph = construct_graph(node_ids_, request_data)
    k = 2
    chain = find_chain_k(graph, k)
    assert len(chain) == k and len(set(chain)) == k

    for i in range(len(chain) - 1):
        if request_data[chain[i]][1] != request_data[chain[i + 1]][0]:
            print("Chain is not valid")
            print(chain[i], chain[i+1])
    print(f"Chain {k}: {chain}")

    print(f"{k}-chain: {find_k_chain_outcome(graph, 6, k)}")
