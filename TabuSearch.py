from Parameters import *
from copy import *
from Solution import solution
from random import random
from random import randrange


class tabu_search:
    def __init__(self, _input_form):
        self.input_form = _input_form
        self.n_nodes = len(_input_form)
        self.solution = self.ts_algorithm()

    def ts_algorithm(self):
        current = solution(self.input_form)  # Use get_initial_solution function
        best = copy(current)
        tabu_list = {}  # A dictionary: key-> the tuple of two nodes being tweaked, whereas the value is the iteration
        # when tweak has occurred
        iteration_counter = 1
        while iteration_counter <= number_of_iterations:
            tweak_counter = 1
            current_tweak = copy(current)
            tweak_feature_list = list()  # this should contain a list should a tuples of nodes being tweaked
            while tweak_counter <= number_of_tweaks:
                # node1, node2, new_solution = self.tweak()
                node1 = randrange(1, 100)
                node2 = randrange(1, 100)
                key = str(node1) + '-' + str(node2)
                value = iteration_counter
                feature = [key, value]
                tweak_feature_list.append(feature)
                # if quality of next better than current_tweak set  current_tweak = next
                tweak_counter += 1
            current = copy(current_tweak)
            for tf in tweak_feature_list:
                tabu_list[tf[0]] = tf[1]
            # if quality of current better than best set best = current
            iteration_counter += 1
        return best

    def tweak(self):
        return 1
