from typing import List

from graph import Node, Graph, construct_graph


def find_longest_chain(graph: Graph):
    max_chain_length = 0
    max_chain = []

    def dfs(current_node: Node, current: List[str]):
        if current_node.out_requests.issubset(current):
            nonlocal max_chain_length
            nonlocal max_chain
            if len(current) > max_chain_length:
                max_chain_length = len(current)
                max_chain = current.copy()
                return

        for request_id in current_node.out_requests:
            if request_id not in current:
                current.append(request_id)
                dfs(graph.requests[request_id].dst, current)
                current.pop()

    for node in graph.nodes.values():
        dfs(node, [])

    return max_chain


def find_longest_chain_no_removals(graph: Graph):
    """
    Find the longest chain without accurately removing requests from paths - polynomial time
    """
    max_chain_length = 0
    max_chain = []
    visited = set()

    def dfs(current_node: Node, current: List[str]):
        if current_node.out_requests.issubset(visited):
            nonlocal max_chain_length
            nonlocal max_chain
            if len(current) > max_chain_length:
                max_chain_length = len(current)
                max_chain = current.copy()
                return

        for request_id in current_node.out_requests:
            if request_id not in visited:
                visited.add(request_id)
                current.append(request_id)
                dfs(graph.requests[request_id].dst, current)
                current.pop()

    for node in graph.nodes.values():
        dfs(node, [])

    return max_chain


if __name__ == "__main__":
    node_ids_ = ["A", "B", "C", "D", "E", "F", "G", "H"]
    request_data_ = {
        "1": ("D", "B"),
        "2": ("E", "C"),
        "3": ("B", "C"),
        "4": ("F", "E"),
        "5": ("C", "E"),
        "6": ("B", "D"),
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
    }
    graph_ = construct_graph(["A", "B", "C", "D"], request_data_)
    print(find_longest_chain(graph_))
    print(find_longest_chain_no_removals(graph_))
