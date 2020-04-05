from Parameters import *
from copy import *
from Solution import Solution
import random


class TabuSearch:
    def __init__(self, _adjacency_list):
        self.adjacency_list = _adjacency_list
        self.n_nodes = len(_adjacency_list)

    def ts_algorithm(self):
        current = Solution(self.adjacency_list)  # Use get_initial_solution function
        best = deepcopy(current)
        tabu_list = {}  # A dictionary: key-> the tuple of two nodes being tweaked, whereas the value is the iteration
        iteration_counter = 1
        while iteration_counter <= number_of_iterations:
            tweak_counter = 1
            current_tweak = deepcopy(current)
            tweak_feature_list = list()  # this should contain a list should a tuples of nodes being tweaked
            while tweak_counter <= number_of_tweaks:
                node1, node2, feature, new_solution = self.move(current_tweak, tabu_list, iteration_counter)
                tweak_feature_list.append(feature)
                if new_solution.fitness <= current_tweak.fitness:
                    current_tweak = deepcopy(new_solution)
                tweak_counter += 1
            current = deepcopy(current_tweak)
            for tf in tweak_feature_list:
                tabu_list[tf[0]] = tf[1]
            if current.fitness < best.fitness:
                best = deepcopy(current)
                print("Best fitness: ", best.fitness)
            iteration_counter += 1
        return best

    def move(self, s: Solution, tabu_list, iteration_counter):
        result: Solution = deepcopy(s)
        feature = list()
        tmp_array = list(range(1, len(s.representation) + 1))
        leafs = list(set(tmp_array) - set(s.representation))
        leafs = list(set(leafs) - set([s.root]))
        legal_move_generated = False
        while not legal_move_generated:
            node1 = random.choice(leafs)
            node2 = random.randint(0, len(s.representation))
            while node1 == node2:
                node2 = random.randint(0, len(s.representation))
            key = str(node1) + '-' + str(node2)
            value = iteration_counter
            feature = [key, value]
            if not self.is_tabu(key, tabu_list, iteration_counter):
                if self.is_legal_move(node1, node2, s):
                    result.representation[node1 - 1] = deepcopy(node2)
                    result.fitness = self.calculate_full_fitness(s)
                    legal_move_generated = True
        return node1, node2, feature, result

    @staticmethod
    def is_tabu(key, tabu_list, iteration):
        if key not in tabu_list.keys():
            return False
        if iteration - tabu_list[key] <= tabu_list_length:
            return True
        else:
            return False

    def is_legal_move(self, _point, _parent, s: Solution):
        all_node_parent = self.find_all_parents(_point, s)
        all_parent_parent = self.find_all_parents_include(_parent, s)
        for pp in all_parent_parent:
            if pp in all_node_parent:
                all_node_parent.remove(pp)
        for old_parent in all_node_parent:
            if _point in self.adjacency_list[old_parent]:
                return False
        return True

    @staticmethod
    def calculate_full_fitness(s: Solution):
        tmp_array = list(range(1, len(s.representation) + 1))
        leafs = list(set(tmp_array) - set(s.representation))
        leafs = list(set(leafs) - set([s.root]))
        all_fitness_values = []
        for leaf in leafs:
            _value = 2
            _parent = s.representation[leaf - 1]
            while s.representation[_parent - 1] != 0:
                _value = _value + 1
                _parent = s.representation[_parent - 1]
            all_fitness_values.append(_value)
        result = max(all_fitness_values)
        return result

    @staticmethod
    def find_all_parents(_node, s: Solution):
        _parents = []
        _parent = s.representation[_node - 1]
        if s.representation[_node - 1] != 0:
            _parents.append(_parent)
        while s.representation[_parent - 1] != 0:
            _parent = s.representation[_parent - 1]
            _parents.append(_parent)
        return _parents

    @staticmethod
    def find_all_parents_include(_node, s: Solution):
        _parents = [_node]
        _parent = s.representation[_node - 1]
        _parents.append(_parent)
        while s.representation[_parent - 1] != 0:
            _parent = s.representation[_parent - 1]
            _parents.append(_parent)
        return _parents
