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

    k = H.edges
    J = nx.empty_graph()
    num_edges_deleted = len(k)
    edges = sorted(H.edges, key=lambda x: H.edges[x[0], x[1]]["weight"])
    while not nx.is_empty(J) and not nx.is_connected(J) and num_edges_deleted > k_num:
        edge = edges.pop()
        J.add_edge(edge)
        k.remove(edge)
        num_edges
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
    inputs = glob.glob('inputs/large/*')
    for input_path in inputs:
        output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
