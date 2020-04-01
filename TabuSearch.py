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
        self.tabu_list = {}  # A dictionary: key-> the tuple of two nodes being tweaked, whereas the value is the iteration

    def ts_algorithm(self):
        current = solution(self.input_form)  # Use get_initial_solution function
        best = copy(current)
        # when tweak has occurred
        iteration_counter = 1
        while iteration_counter <= number_of_iterations:
            tweak_counter = 1
            current_tweak = copy(current)
            tweak_feature_list = list()  # this should contain a list should a tuples of nodes being tweaked
            while tweak_counter <= number_of_tweaks:
                #implement
                node1, node2, next_solution = self.tweak(current_tweak,iteration_counter)
                key = str(node1) + '-' + str(node2)
                value = iteration_counter
                feature = [key, value]
                tweak_feature_list.append(feature)
                # if quality of next better than current_tweak set  current_tweak = next##

                ##########################################################################
                tweak_counter += 1
            current = copy(current_tweak)
            for tf in tweak_feature_list:
                self.tabu_list[tf[0]] = tf[1]
            # if quality of current better than best set best = current

            iteration_counter += 1
        return best

    def tweak(self,_solution,_iteration):
        tmp_array = list(range(1, len(self.input_form)+1))
        leafs = list(set(tmp_array) - set(_solution.representation))
        leafs = list(set(leafs) - set([_solution.root]))
        random_leaf = random.choice(leafs)
        random_parent = random.randint(0,len(_solution.representation))
        while random_leaf == random_parent:
            random_parent = random.randint(0,len(self.solution))
        if self.is_tabu(random_leaf,_iteration):
            return False
        if self.is_legal_move(random_leaf,random_parent):
            _solution.representation[random_leaf-1] = copy.copy(random_parent)
        _solution.calculate_fitness()
        return random_leaf, random_parent, _solution


    def is_legal_move(self,_point,_parent):
        all_point_siblings = self.find_all_parents(_point)
        all_parent_siblings = self.find_all_parents_include(_parent)
        for parent_sibling in all_parent_siblings:
            if parent_sibling in all_point_siblings:
                all_point_siblings.remove(parent_sibling)
        for point_sibling in all_point_siblings:
            if _point in self.input_form[point_sibling]:
                return False
        return True

    def is_tabu(self,_key,_iteration):
        if _key not in self.tabu_list:
            return False
        if _iteration - self.tabu_list[_key] >= tabu_list_length:
            return False
        return True
