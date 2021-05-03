import networkx as nx
from networkx.algorithms.components.connected import is_connected
from parse import read_input_file, read_output_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


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

    for _ in range(c_num):
        curr_shortest = nx.shortest_path(H, 0, num_nodes - 1, weight="weight")
        if len(curr_shortest) == 2:
            break
        find_sum_weights = lambda x: sum([H.edges[x, i]["weight"] for i in H.adj[x] if i != 0 and i != num_nodes - 1])
        least_weight = min(curr_shortest[1:-1], key=find_sum_weights)
        H_cp = H.copy()
        H_cp.remove_node(least_weight)
        if not nx.is_connected(H_cp):
            break
        H.remove_node(least_weight)
        c.append(least_weight)

    for _ in range(k_num):
        curr_shortest = nx.shortest_path(H, 0, num_nodes - 1, weight="weight")
        pg = nx.path_graph(curr_shortest)
        min_edge_src, min_edge_dest = min(pg.edges, key=lambda x: H.edges[x[0], x[1]]["weight"])
        H_cp = H.copy()
        H_cp.remove_edge(min_edge_src, min_edge_dest)
        if not nx.is_connected(H_cp):
            break
        H.remove_edge(min_edge_src, min_edge_dest)
        k.append((min_edge_src, min_edge_dest))
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
