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


