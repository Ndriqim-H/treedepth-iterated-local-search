from Parameters import *
from copy import *
from Solution import solution
from random import random


class tabu_search:
    def __init__(self, _n_nodes):
        self.n_nodes = _n_nodes
        self.solution = list()

    def ts_algorithm(self, n_nodes: int):
        current = solution(n_nodes)  # Use get_initial_solution function
        best = copy(current)
        tabu_list = {}  # A dictionary: key-> the tuple of two nodes being tweaked, whereas the value is the iteration
        # when tweak has ocurred
        iteration_counter = 1
        while iteration_counter <= number_of_iterations:
            tweak_counter = 1
            current_tweak = copy(current)
            tweak_feature_list = list()  # this should contain a list should a tuples of nodes being tweaked
            while tweak_counter <= number_of_tweaks:
                next = list()  # current_tweak current solution
                # Add this tweak tuple to tweak_feature_list
                # if quality of next better than current_tweak set  current_tweak = next
            current = copy(current_tweak)
            for tf in tweak_feature_list:
                # Update the tabu_list for all features
                pass
            # if quality of current better than best set best = current
        return best

    def get_initial_solution(self, _n_nodes: int):
        random_array = random.sample(range(1, _n_nodes + 1), _n_nodes)
        result = solution(_n_nodes)
        # ...
        self.solution[self.root - 1] = 0
        random_array.remove(self.root)
        random.shuffle(random_array)
        _parent = copy.copy(self.root)
        for i in range(0, len(random_array)):
            self.solution[random_array[i] - 1] = copy.copy(_parent)
            _parent = copy.copy(random_array[i])
        return result
