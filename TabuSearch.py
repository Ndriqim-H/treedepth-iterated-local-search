from Parameters import *
from copy import *
from Solution import solution
from random import random


class tabu_search:
    def __init__(self, _input_form):
        self.input_form = _input_form
        self.n_nodes = len(_input_form)
        self.solution = list()

    def ts_algorithm(self):
        current = solution(self.input_form)  # Use get_initial_solution function
        best = copy(current)
        tabu_list = {}  # A dictionary: key-> the tuple of two nodes being tweaked, whereas the value is the iteration
        # when tweak has ocurred
        iteration_counter = 1
        while iteration_counter <= number_of_iterations:
            tweak_counter = 1
            current_tweak = copy(current)
            tweak_feature_list = list()  # this should contain a list should a tuples of nodes being tweaked
            while tweak_counter <= number_of_tweaks:
                node, parent, new_solution = self.tweak()
                next = list()  # current_tweak current solution
                # Add this tweak tuple to tweak_feature_list
                # if quality of next better than current_tweak set  current_tweak = next
            current = copy(current_tweak)
            for tf in tweak_feature_list:
                # Update the tabu_list for all features
                pass
            # if quality of current better than best set best = current
        return best

    def tweak(self):
        return 1

