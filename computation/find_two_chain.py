import copy

from graph import Graph, construct_graph


def find_two_chain_outcome(graph: Graph, time_limit: int):
    graph_ = copy.deepcopy(graph)  # deepcopy to avoid removing edges from the original graph
    served = 0  # number of requests served
    time_remaining = time_limit
    jump_needed = False

    while time_remaining > 0 and len(graph_.requests):
        two_chain = find_chain_two(graph_)
        print(two_chain)
        if not two_chain:
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

        if time_remaining <= 2:
            served += time_remaining
            return served
        else:
            served += 2
            time_remaining -= 2
            chain_endpoint = graph_.requests[two_chain[1]].dst
            for request_id in two_chain:
                graph_.remove_request(request_id)
            while time_remaining > 0 and len(graph_.requests) and chain_endpoint.out_requests:
                request_id = list(chain_endpoint.out_requests)[0]
                print(request_id)
                chain_endpoint = graph_.requests[request_id].dst
                graph_.remove_request(request_id)
                served += 1
                time_remaining -= 1

    return served


def find_chain_two(graph: Graph):
    for request in graph.requests.values():
        if request.dst.out_requests:
            return [request.id, list(request.dst.out_requests)[0]]
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
    print(f"TwoChain: {find_two_chain_outcome(graph, 28)}")
