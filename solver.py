import networkx as nx
from networkx.algorithms.components.connected import is_connected
from parse import read_input_file, read_output_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import time


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

    ctr = 0
    while c_num > 0 and ctr < 10:
        # short_paths = list(nx.shortest_simple_paths(H, 0, num_nodes - 1, weight="weight"))
        shortest_dict = nx.shortest_path(H, 0, weight="weight")
        shortest_adj_paths = []
        for adjacent in list(G.neighbors(num_nodes-1)):
            shortest_adj_paths.append(shortest_dict[adjacent])
        curr_remaining = [set(i[1:-1]) for i in shortest_adj_paths[:-1] if len(i) > 2]
        found_node = set.intersection(*curr_remaining)
        if found_node != set():
            c.append(list(found_node)[0])
            H_cp = H.copy()
            H_cp.remove_node(list(found_node)[0])
            if nx.is_connected(H_cp):
                H.remove_node(list(found_node)[0])
            ctr += 1
            break
        while found_node == set():
            curr_remaining = curr_remaining[:-1]
            found_node = set.intersection(*curr_remaining)
        H.remove_node(list(found_node)[0])
        H_cp = H.copy()
        H_cp.remove_node(list(found_node)[0])
        if nx.is_connected(H_cp):
            H.remove_node(list(found_node)[0])
        else: 
            ctr += 1
        c_num -= 1

    # H_cp = H.copy()
    # max_spanning_tree = nx.maximum_spanning_tree(H_cp, weight="weight")
    # H_cp.remove_edges_from(list(max_spanning_tree.edges))
    # k = sorted(list(H_cp.edges), key=lambda x: H_cp.edges[x[0], x[1]]["weight"])[:k_num]
    # H.remove_edges_from(k)

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

if __name__ == '__main__':
    try:
        inputs = glob.glob(f'inputs/{sys.argv[1]}/*')
        scores = []
        start = time.time()
        for input_path in inputs:
            output_path = f'outputs/{sys.argv[1]}/' + basename(normpath(input_path))[:-3] + '.out'
            G = read_input_file(input_path)
            c, k = solve(G)
            assert is_valid_solution(G, c, k)
            distance = calculate_score(G, c, k)
            write_output_file(G, c, k, output_path)
            scores.append(distance)
        end = time.time()
        print(f"Elapsed: {end - start} s\nMaximum score: {max(scores)}\nMinimum score: {min(scores)}\nAverage score: {sum(scores) / len(scores)}")
    except IndexError:
        print("Empty size argument")
