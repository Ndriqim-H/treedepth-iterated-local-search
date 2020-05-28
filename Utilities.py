from Solution import Solution
import Parameters
import random
import sys

# import networkx as nx

node_list = list()
edge_list = list()


def get_sample_solution():
    sample_root = 9
    sample_representation1 = [[3], [4], [5], [], [0, 2], []]
    sample_representation2 = [[1, 4], [], [3], [0], [5], []]
    sample_representation3 = [[3], [0, 2], [5], [], [1], []]
    sample_representation4 = [[4, 1, 6, 7], [], [3], [0], [], [2], [8], [], [], [5]]
    sample_fitness = -1
    result = Solution(sample_root, sample_representation4, sample_fitness)
    return result


def get_fitness(representation, root):
    result = 1 + calculate_fitness(representation, root)
    return result


def calculate_fitness(representation, parent):
    child_list = representation[parent]
    if len(child_list) == 0:
        fitness = 0
    elif len(child_list) == 1:
        fitness = 1 + calculate_fitness(representation, child_list[0])
    else:
        max_fitness = -1
        for child in child_list:
            current_fitness = 1 + calculate_fitness(representation, child)
            if current_fitness > max_fitness:
                max_fitness = current_fitness
        fitness = max_fitness
    return fitness


def get_adjacency_list(file_name):
    adjacency_list = {}
    # edge_graph = nx.Graph()
    file = open('instances/' + file_name, 'r')
    first_line = file.readline().split(' ')
    total_points = int(first_line[2])
    node_list.append(int(first_line[2]))
    n_nodes = int(first_line[2])
    edge_list.append(int(first_line[3]))
    n_edges = int(first_line[3])
    fill_adjacency_list(total_points, adjacency_list)
    file_rows = filter(None, file.read().split('\n'))
    for row in file_rows:
        element = row.split(' ')
        node1 = int(element[0]) - 1  # convert node1 to a zero based index
        node2 = int(element[1]) - 1  # convert node2 to a zero based index
        # edge_graph.add_edge(node1, node2)
        if node1 in adjacency_list:
            adjacency_list[node1].append(node2)
        if node2 in adjacency_list:
            adjacency_list[node2].append(node1)
    return adjacency_list, n_nodes, n_edges


def fill_adjacency_list(total_points, adjacency_list):
    for i in range(total_points):
        adjacency_list[i] = []


def convert_to_pace_format(s: Solution):
    result = [-1] * len(s.representation)
    result[s.root] = 0  # revert to one based index
    for i in range(len(s.representation)):
        node_list = s.representation[i]
        if len(node_list) > 0:
            for node in node_list:
                result[node] = i + 1  # revert to one based index
    return result


def save_solution(_output_file, formatted_solution: list, fitness):
    file_name = _output_file[0:9]
    file = open('solutions/' + file_name + '.tree', "w+")
    file.write(str(fitness) + "\n")
    for i in formatted_solution:
        file.write(str(i) + "\n")
    file.close()


def count_duplicates_test(representation: list):
    duplicate_list = list()
    for c in range(len(representation)):
        child_list = representation[c]
        for node in child_list:
            if node in duplicate_list:
                return True
            else:
                duplicate_list.append(node)
    return False
