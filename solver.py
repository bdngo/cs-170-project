import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random


def solve(H):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    H = G.copy()
    c, k = [], []
    # finding c and k
    num_nodes = H.number_of_nodes()
    if num_nodes <= 30:
        c_num, k_num = 1, 15
    elif num_nodes <= 50:
        c_num, k_num = 3, 50
    elif num_nodes <= 100:
        c_num, k_num = 5, 100

    best_score = -float("inf")
    seen_nodes = []
    while c_num > 0:
        H_cp = H.copy()
        curr_shortest = nx.shortest_path(H_cp, 0, num_nodes - 1, weight="weight")
        if len(curr_shortest) == 2:  # Exit if shortest path is only 1 edge
            break
        not_seen_nodes = list(set(curr_shortest[1:-1]) - set(seen_nodes))
        if len(not_seen_nodes) == 0:  # Exit if we have seen all nodes
            break
        to_rm = random.choice(not_seen_nodes)
        H_cp.remove_node(to_rm)
        if not nx.is_connected(H_cp): # Reject and pick new node if graph is disconnected
            seen_nodes.append(to_rm)
            continue
        curr_score = nx.shortest_path_length(H_cp, 0, num_nodes - 1, weight="weight") 
        if curr_score < best_score: # Reject and pick new node if score is lower
            seen_nodes.append(to_rm)
            continue
        best_score = curr_score
        H.remove_node(to_rm)
        c.append(to_rm)
        c_num -= 1
        seen_nodes.clear()

    best_score = -float("inf")
    seen_edges = []
    while k_num > 0:
        H_cp = H.copy()
        curr_shortest = nx.shortest_path(H_cp, 0, num_nodes - 1, weight="weight")
        pg = nx.path_graph(curr_shortest)
        not_seen_edges = list(set(pg.edges) - set(seen_edges))
        if len(not_seen_edges) == 0: # Exit if we have seen all edges
            break
        src_rm, dst_rm = random.choice(list(not_seen_edges))
        H_cp.remove_edge(src_rm, dst_rm)
        if not nx.is_connected(H_cp): # Reject and pick new edge if graph is disconnected
            seen_edges.append((src_rm, dst_rm))
            continue
        curr_score = nx.shortest_path_length(H_cp, 0, num_nodes - 1, weight="weight")
        if curr_score < best_score: # Reject and pick new edge if score is lower
            seen_edges.append((src_rm, dst_rm))
            continue
        best_score = curr_score
        H.remove_edge(src_rm, dst_rm)
        k.append((src_rm, dst_rm))
        k_num -= 1
        seen_edges.clear()

    return c, k


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print(f"Shortest Path Difference: {calculate_score(G, c, k)}")
#     write_output_file(G, c, k, 'outputs/small-1.out')

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    try:
        inputs = glob.glob(f'inputs/{sys.argv[1]}/*')
        for input_path in inputs:
            output_path = f'outputs/{sys.argv[1]}/' + basename(normpath(input_path))[:-3] + '.out'
            G = read_input_file(input_path)
            c, k = solve(G)
            assert is_valid_solution(G, c, k)
            distance = calculate_score(G, c, k)
            write_output_file(G, c, k, output_path)
    except IndexError:
        print("Empty size argument")
