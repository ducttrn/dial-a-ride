import copy

from graph import Graph, construct_graph


def find_k_chain_outcome(graph: Graph, time_limit: int, k: int):
    graph_ = copy.deepcopy(graph)  # deepcopy to avoid removing edges from the original graph
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0 and len(graph_.requests):
        chain_to_serve = None
        while not chain_to_serve and k > 1:
            chain_to_serve = find_chain_k(graph_, k)
            if not chain_to_serve:
                k -= 1

        print(chain_to_serve)

        if not chain_to_serve:
            # Serve single chains
            while time_remaining > 0 and len(graph_.requests):
                if jump_needed:
                    time_remaining -= 1
                served += 1
                time_remaining -= 1
                print(list(graph_.requests.keys())[0])
                graph_.remove_request(list(graph_.requests.keys())[0])
                jump_needed = True
            return served

        if jump_needed:
            time_remaining -= 1
        else:
            jump_needed = True

        if time_remaining <= len(chain_to_serve):
            served += time_remaining
            return served
        else:
            served += len(chain_to_serve)
            time_remaining -= len(chain_to_serve)
            chain_endpoint = graph_.requests[chain_to_serve[-1]].dst
            for request_id in chain_to_serve:
                graph_.remove_request(request_id)
            while time_remaining > 0 and len(graph_.requests) and chain_endpoint.out_requests:
                request_id = list(chain_endpoint.out_requests)[0]
                print(request_id)
                chain_endpoint = graph_.requests[request_id].dst
                graph_.remove_request(request_id)
                served += 1
                time_remaining -= 1

    return served


def find_chain_k(graph: Graph, k: int):

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
        chain = find_chain_k_(k - 1, [request.id])
        if chain:
            return chain

    return []


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
    k = 15
    chain = find_chain_k(graph, k)
    assert len(chain) == k and len(set(chain)) == k
    for i in range(len(chain) - 1):
        if request_data[chain[i]][1] != request_data[chain[i + 1]][0]:
            print("Chain is not valid")
            print(chain[i], chain[i+1])
    print(f"Chain {k}: {chain}")

    print(f"{k}-chain: {find_k_chain_outcome(graph, 23, k)}")
