from graph import Node, Graph, construct_graph


def find_longest_chain(graph: Graph):
    max_chain_length = 0
    max_chain = set()

    def dfs(current_node: Node, served: set[str], current_chain_length: int):
        if current_node.out_requests.issubset(served):
            nonlocal max_chain_length
            nonlocal max_chain
            if current_chain_length > max_chain_length:
                max_chain_length = current_chain_length
                max_chain = served.copy()
                return

        for request_id in current_node.out_requests:
            if request_id not in served:
                served.add(request_id)
                dfs(graph.requests[request_id].dst, served, current_chain_length + 1)
                served.remove(request_id)

    for node in graph.nodes.values():
        dfs(node, set(), 0)

    return max_chain, max_chain_length

def find_longest_chain_no_removals(graph: Graph):
    max_chain_length = 0
    max_chain = set()

    def dfs(current_node: Node, served: set[str], current_chain_length: int):
        if current_node.out_requests.issubset(served):
            nonlocal max_chain_length
            nonlocal max_chain
            if current_chain_length > max_chain_length:
                max_chain_length = current_chain_length
                max_chain = served.copy()
                return

        for request_id in current_node.out_requests:
            if request_id not in served:
                served.add(request_id)
                dfs(graph.requests[request_id].dst, served, current_chain_length + 1)

    for node in graph.nodes.values():
        dfs(node, set(), 0)

    return max_chain, max_chain_length


if __name__ == "__main__":
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

    graph_ = construct_graph(node_ids_, request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))

    # --------------------------------------------------------------------
    request_data_ = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "F"),
        "8": ("F", "G"),
        "9": ("G", "F"),
        "10": ("G", "H"),
    }

    graph_ = construct_graph(node_ids_, request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))

    # --------------------------------------------------------------------
    request_data_ = {
        "1": ("A", "B"),
        "2": ("B", "C"),
        "3": ("C", "D"),
        "4": ("B", "G"),
        "5": ("E", "F"),
        "6": ("F", "G"),
        "7": ("G", "F"),
        "8": ("F", "G"),
        "9": ("G", "F"),
        "10": ("G", "H"),
        "11": ("G", "C"),
    }
    graph_ = construct_graph(node_ids_, request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))

    # --------------------------------------------------------------------
    request_data_ = {
        "1": ("A", "B"),
        "2": ("A", "F"),
        "3": ("A", "E"),
        "4": ("B", "E"),
        "5": ("C", "E"),
        "6": ("B", "C"),
        "7": ("C", "D"),
        "8": ("D", "B"),
    }
    graph_ = construct_graph(["A", "B", "C", "D", "E", "F"], request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))

    # --------------------------------------------------------------------
    request_data_ = {
        "1": ("D", "A"),
        "2": ("D", "B"),
        "3": ("D", "C"),
    }
    graph_ = construct_graph(["A", "B", "C", "D"], request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))
