from Solution import Solution
import Parameters
import random
import sys


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
    file = open('instances/' + file_name + '.gr', 'r')
    first_line = file.readline().split(' ')
    total_points = int(first_line[2])
    fill_adjacency_list(total_points, adjacency_list)
    file_rows = filter(None, file.read().split('\n'))
    for row in file_rows:
        element = row.split(' ')
        node1 = int(element[0]) - 1  # convert node1 to a zero based index
        node2 = int(element[1]) - 1  # convert node2 to a zero based index
        if node1 in adjacency_list:
            adjacency_list[node1].append(node2)
        if node2 in adjacency_list:
            adjacency_list[node2].append(node1)
    return adjacency_list


def fill_adjacency_list(total_points, adjacency_list):
    for i in range(total_points):
        adjacency_list[i] = []


def get_initial_solution(adjacency_list: dict):
    n_nodes = len(adjacency_list)
    random_node_list = random.sample(range(0, n_nodes), n_nodes)
    # random_node_list = [0, 4, 1, 6, 7, 9, 8, 5, 2, 3]
    # random_node_list = [5, 7, 11, 10, 1, 3, 4, 14, 16, 2, 9, 8, 13, 15, 0, 6, 12]  # exact 003
    print(random_node_list)
    representation = list()
    for i in range(n_nodes):
        lst = list()
        representation.append(lst)
    root = random_node_list[0]
    first_child = random_node_list[1]
    representation[root].append(first_child)
    for n in range(2, n_nodes, 1):
        node = random_node_list[n]
        shift_node_up = False
        node_to_link, shift_node_up = find_node_to_link(adjacency_list, representation, root, root, node, shift_node_up)
        if shift_node_up:
            child_list = representation[node_to_link]
            representation[node_to_link] = list()
            representation[node_to_link].append(node)
            representation[node] = list(child_list)
        else:
            representation[node_to_link].append(node)
    fitness = get_fitness(representation, root)
    result = Solution(root, representation, fitness)
    return result


def find_node_to_link(adjacency_list: dict, representation, parent, current_node_to_link, node, shift_node_up):
    node_to_link = current_node_to_link
    child_list = representation[parent]
    if len(child_list) == 0:
        return node_to_link, shift_node_up
    elif len(child_list) == 1:
        node_to_link_candidate = child_list[0]
        if node in adjacency_list[node_to_link_candidate]:
            node_to_link = node_to_link_candidate
        node_to_link, shift_node_up = find_node_to_link(adjacency_list, representation, node_to_link_candidate,
                                                        node_to_link, node, shift_node_up)
    else:
        num_paths = 0
        for child in child_list:
            previous_node_to_link = node_to_link
            if node in adjacency_list[child]:
                node_to_link = child
            node_to_link, shift_node_up = find_node_to_link(adjacency_list, representation, child, node_to_link, node,
                                                            shift_node_up)
            if previous_node_to_link != node_to_link:
                num_paths += 1
                if num_paths == 2:
                    node_to_link = parent
                    shift_node_up = True
                    break
    return node_to_link, shift_node_up


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
    file = open('solutions/' + _output_file + '.tree', "w+")
    file.write(str(fitness) + "\n")
    for i in formatted_solution:
        file.write(str(i) + "\n")
    file.close()


def main():
    sys.setrecursionlimit(1000000000)
    for i in range(Parameters.instance_index, Parameters.instance_index+2, 2):
        instance_name = "heur_" + "{0:03}".format(i)
        adjacency_list = get_adjacency_list(instance_name)
        print(adjacency_list)
        s = get_initial_solution(adjacency_list)
        print("Representation: ", s.representation)
        print("Root: ", s.root)
        print("Fitness: ", s.fitness)
        print("recursion limit:", sys.getrecursionlimit())
        formatted_solution = convert_to_pace_format(s)
        save_solution(instance_name, formatted_solution, s.fitness)


main()
