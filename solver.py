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

    node_ctr = 0
    while c_num > 0:
        if node_ctr > len(H.nodes):
            break
        H_cp = H.copy()
        curr_shortest = nx.shortest_path(H_cp, 0, num_nodes - 1)
        if len(curr_shortest) == 2:
            break
        to_rm = random.choice(curr_shortest[1:-1])
        H_cp.remove_node(to_rm)
        if not nx.is_connected(H_cp):
            node_ctr += 1
            continue
        H.remove_node(to_rm)
        c.append(to_rm)
        c_num -= 1

    edge_ctr = 0
    while k_num > 0:
        if edge_ctr > len(H.edges):
            break
        H_cp = H.copy()
        curr_shortest = nx.shortest_path(H_cp, 0, num_nodes - 1)
        pg = nx.path_graph(curr_shortest)
        src_rm, dst_rm = random.choice(list(pg.edges))
        H_cp.remove_edge(src_rm, dst_rm)
        if not nx.is_connected(H_cp):
            edge_ctr += 1
            continue
        H.remove_edge(src_rm, dst_rm)
        k.append((src_rm, dst_rm))
        k_num -= 1

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
