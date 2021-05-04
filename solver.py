import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import time
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
    num_nodes = H.number_of_nodes()
    if num_nodes <= 30:
        c_num, k_num = 1, 15
    elif num_nodes <= 50:
        c_num, k_num = 3, 50
    elif num_nodes <= 100:
        c_num, k_num = 5, 100

    ctr = 0
    while c_num > 0 and ctr < 10:
        H_cp = H.copy()
        H_cp.remove_node(num_nodes-1)
        shortest_dict = nx.shortest_path(H_cp, 0, weight="weight")
        #shortest_adj_paths = [shortest_dict[i] for i in list(H.adj[num_nodes - 1])]
        shortest_adj_paths = [shortest_dict[i] for i in list(H.adj[num_nodes - 1]) if shortest_dict.get(i) != None]
        sorted_paths = sorted(shortest_adj_paths, key=lambda path: sum([H_cp[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)]))
        curr_remaining = [set(i[1:-1]) for i in sorted_paths[:-1] if len(i) > 2]
        if curr_remaining == []:
            break
        found_node = set.intersection(*curr_remaining) - set(sorted_paths[-1])
        if found_node != set():
            chosen_node = random.choice(list(found_node))
            H_cp = H.copy()
            H_cp.remove_node(chosen_node)
            if nx.is_connected(H_cp):
                H.remove_node(chosen_node)
                c.append(chosen_node)
            ctr += 1
            break
        while found_node == set() and len(curr_remaining) > 1:
            curr_remaining = curr_remaining[:-1]
            found_node = set.intersection(*curr_remaining) - set(sorted_paths[-1])
        if found_node == set():
            break
        chosen_node = random.choice(list(found_node))
        H_cp = H.copy()
        H_cp.remove_node(chosen_node)
        if nx.is_connected(H_cp):
            H.remove_node(chosen_node)
            c.append(chosen_node)
        else: 
            ctr += 1
        c_num -= 1

    H_cp = H.copy()
    max_spanning_tree = nx.maximum_spanning_tree(H_cp, weight="weight")
    H_cp.remove_edges_from(list(max_spanning_tree.edges))
    k = sorted(list(H_cp.edges), key=lambda x: H_cp.edges[x[0], x[1]]["weight"])[:k_num]
    H.remove_edges_from(k)
    
    # H_cp = H.copy()
    # for u, v in H_cp.edges:
    #     H.edges[u, v]["weight"] *= -1
    # _, paths = nx.single_source_bellman_ford(H_cp, 0, weight="weight")
    # max_paths_tree = nx.Graph()
    # for path in paths.values():
    #     nx.add_path(max_paths_tree, path, weight="weight")
    # for u, v in max_paths_tree.edges:
    #     max_paths_tree.edges[u, v]["weight"] *= -1
    # H_cp.remove_edges_from(list(max_paths_tree.edges))
    # k = sorted(list(H_cp.edges), key=lambda x: H_cp.edges[x[0], x[1]]["weight"])[:k_num]
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
