import Parameters
from copy import *
from Solution import Solution
import random
import Utilities
import sys
from operator import itemgetter
from queue import Queue
from queue import LifoQueue
from math import log2
import pandas as pd


class TabuSearch:
    def __init__(self, _adjacency_list):
        self.adjacency_list = _adjacency_list
        self.n_nodes = len(_adjacency_list)
        if Parameters.fully_random_initial_solution:
            self.number_of_edges_list = random.sample(range(0, self.n_nodes), self.n_nodes)
        else:
            self.number_of_edges_list = self.create_number_of_edges_list()
        self.tabu_list = {}

    def ts_algorithm(self):
        # current = self.get_simple_initial_solution()
        current = self.get_initial_solution()
        best = copy(current)
        iteration_counter = 1
        iteration_no_improvement_counter = 1
        while iteration_counter <= Parameters.number_of_iterations:
            tweak_counter = 1
            current_tweak = copy(current)
            new_solution_node_list = list()
            while tweak_counter <= Parameters.number_of_tweaks:
                selected_nodes, node_type = self.select_nodes(current_tweak, iteration_counter)
                new_solution = self.move_node(current_tweak, selected_nodes, node_type)
                if new_solution.fitness <= current_tweak.fitness:
                    current_tweak = copy(new_solution)
                    new_solution_node_list = selected_nodes
                tweak_counter += 1
            current = copy(current_tweak)
            # print("current fitness: ", current.fitness)
            for used_node in new_solution_node_list:
                if used_node in current.representation[current.root]:
                    used_node_parent = current.root
                else:
                    used_node_parent = self.find_non_root_parent_node(current.representation, used_node)
                tabu_feature = str(used_node) + '-' + str(used_node_parent)
                self.tabu_list[tabu_feature] = iteration_counter
            if current.fitness < best.fitness:
                best = copy(current)
                print("Best fitness: ", best.fitness)
                iteration_no_improvement_counter = 0
                # Parameters.insert_nodes_in_random_order = False
                # Parameters.insert_nodes_in_descending_order = True
                Parameters.max_number_of_paths = 50
            else:
                iteration_no_improvement_counter += 1
            if iteration_no_improvement_counter % Parameters.number_of_iterations_with_no_improvement == 0:
                current = self.perturb(best, iteration_counter, iteration_no_improvement_counter)
                # Parameters.insert_nodes_in_random_order = not Parameters.insert_nodes_in_random_order
                # Parameters.insert_nodes_in_descending_order = not Parameters.insert_nodes_in_descending_order
                Parameters.max_number_of_paths = Parameters.max_number_of_paths_list[
                    random.randrange(0, len(Parameters.max_number_of_paths_list))]
            iteration_counter += 1
        return best

    def perturb(self, s: Solution, iteration_counter, iteration_no_improvement_counter):
        current_solution = copy(s)
        additional_perturbations = int(log2(
            int(1 + iteration_no_improvement_counter / Parameters.number_of_iterations_with_no_improvement)))
        # print("test - additional_perturbations:", additional_perturbations)
        for i in range(Parameters.minimal_perturb_intensity + additional_perturbations):
            selected_nodes, node_type = self.select_nodes(current_solution, iteration_counter)
            new_solution = self.move_node(current_solution, selected_nodes, node_type)
            additional_deprecation = additional_perturbations / 100
            # print("test - additional_deprecation: ",additional_deprecation)
            if new_solution.fitness * (
                    Parameters.perturbed_solution_deprecation_percentage - additional_deprecation) < current_solution.fitness:
                current_solution = copy(new_solution)
        return current_solution

    def get_key(self, new_solution: Solution):
        key = self.solution_node_sequence(new_solution.representation, new_solution.root)
        return key

    def solution_node_sequence(self, representation, parent):
        child_list = representation[parent]
        if len(child_list) == 0:
            result = ''
        elif len(child_list) == 1:
            result = str(child_list[0]) + self.solution_node_sequence(representation, child_list[0])
        else:
            for child in child_list:
                result = str(child) + self.solution_node_sequence(representation, child)
        return result

    def select_nodes(self, s: Solution, iteration_counter):
        tabu_status = True
        while tabu_status:
            random_number = random.randrange(0, 101)
            if random_number <= Parameters.node_type_selection_probability['subtree']:
                selected_nodes = self.get_sub_tree_nodes(s.representation, s.fitness, s.root)
                node_type = 'subtree'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal']:
                selected_nodes = [self.get_internal_node(s.representation, s.root)]
                node_type = 'internal'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf']:
                selected_nodes = [self.get_leaf_node(s.representation)]
                node_type = 'leaf'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root']:
                selected_nodes = [s.root]
                node_type = 'root'
                tabu_status = False
                break
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root'] + \
                    Parameters.node_type_selection_probability['top']:
                selected_nodes = self.get_top_nodes(s)
                node_type = 'top'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root'] + \
                    Parameters.node_type_selection_probability['top'] + \
                    Parameters.node_type_selection_probability['level']:
                selected_nodes = self.get_level_nodes(s)
                node_type = 'level'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root'] + \
                    Parameters.node_type_selection_probability['top'] + \
                    Parameters.node_type_selection_probability['level'] + \
                    Parameters.node_type_selection_probability['path']:
                selected_nodes = self.get_longer_path_nodes(s)
                node_type = 'path'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root'] + \
                    Parameters.node_type_selection_probability['top'] + \
                    Parameters.node_type_selection_probability['level'] + \
                    Parameters.node_type_selection_probability['path'] + \
                    Parameters.node_type_selection_probability['leafs']:
                selected_nodes = self.get_leaf_nodes(s.representation)
                node_type = 'leafs'
            elif random_number <= Parameters.node_type_selection_probability['subtree'] + \
                    Parameters.node_type_selection_probability['internal'] + \
                    Parameters.node_type_selection_probability['leaf'] + \
                    Parameters.node_type_selection_probability['root'] + \
                    Parameters.node_type_selection_probability['top'] + \
                    Parameters.node_type_selection_probability['level'] + \
                    Parameters.node_type_selection_probability['path'] + \
                    Parameters.node_type_selection_probability['leafs'] + \
                    Parameters.node_type_selection_probability['partial_path']:
                selected_nodes = self.get_partial_path_nodes(s)
                node_type = 'partial_path'
            else:
                selected_nodes = self.get_bottom_nodes(s)
                node_type = 'bottom'
            for n in selected_nodes:
                tabu_feature = str(n) + '-' + str(s.root)
                tabu_status = self.is_tabu(tabu_feature, iteration_counter)
                if tabu_status:
                    break
        return selected_nodes, node_type

    @staticmethod
    def get_top_nodes(s: Solution):
        result = list()
        q_parents = Queue()
        q_parents.put([s.root])
        top_depth = random.randrange(2, int(s.fitness * Parameters.top_max_limit_probability) + 1)
        for d in range(top_depth):
            parents = q_parents.get()
            children = list()
            for parent in parents:
                result.append(parent)
                for c in s.representation[parent]:
                    children.append(c)
            q_parents.put(children)
        return result

    @staticmethod
    def get_level_nodes(s: Solution):
        q_parents = Queue()
        q_parents.put([s.root])
        depth_level = random.randrange(2, s.fitness + 1)
        for d in range(depth_level):
            parents = q_parents.get()
            children = list()
            for parent in parents:
                for c in s.representation[parent]:
                    children.append(c)
            q_parents.put(children)
        return parents

    @staticmethod
    def get_path_nodes(s: Solution):
        result = list()
        parent = s.root
        leaf_level_reached = False
        while not leaf_level_reached:
            result.append(parent)
            child_list = s.representation[parent]
            if len(child_list) > 0:
                child = child_list[random.randrange(0, len(child_list))]
                parent = child
            else:
                leaf_level_reached = True
        return result

    def get_longer_path_nodes(self, s: Solution):
        result = self.get_path_nodes(s)
        max_path = len(result)
        for i in range(random.randrange(1, Parameters.max_number_of_paths)):
            node_to_move_list = self.get_path_nodes(s)
            if len(node_to_move_list) > max_path:
                result = node_to_move_list
                max_path = len(node_to_move_list)
        return result

    def get_partial_path_nodes(self, s: Solution):
        all_path_nodes_list = self.get_path_nodes(s)
        max_path = len(all_path_nodes_list)
        for i in range(random.randrange(1, Parameters.max_number_of_paths)):
            node_to_move_list = self.get_path_nodes(s)
            if len(node_to_move_list) > max_path:
                all_path_nodes_list = node_to_move_list
                max_path = len(node_to_move_list)
        all_path_nodes = len(all_path_nodes_list)
        partial_path_start_position = all_path_nodes - random.randrange(1, max(2, int(
            all_path_nodes * Parameters.max_partial_path_length_percentage)))
        result = list()
        # print("path length: ", (all_path_nodes - partial_path_start_position))
        for i in range(partial_path_start_position - 1, all_path_nodes):
            result.append(all_path_nodes_list[i])
        return result

    def get_bottom_nodes(self, s: Solution):
        top_nodes = list()
        q_parents = Queue()
        q_parents.put([s.root])
        bottom_depth = random.randrange(1, max(2, int(s.fitness * Parameters.bottom_depth_max_limit_probability) + 1))
        for d in range(s.fitness - bottom_depth):
            parents = q_parents.get()
            children = list()
            for parent in parents:
                top_nodes.append(parent)
                for c in s.representation[parent]:
                    children.append(c)
            q_parents.put(children)
        result = list(set(self.number_of_edges_list) - set(top_nodes))
        return result

    @staticmethod
    def get_leaf_node(representation: list):
        random_start_index = random.randrange(0, len(representation))
        random_walk = random.randrange(0, int(Parameters.random_walk_limit * len(representation)))
        rw_counter = 0
        node = random_start_index
        while node < len(representation):
            if len(representation[node]) == 0:
                if rw_counter == random_walk:
                    return node
                rw_counter += 1
            if node != len(representation) - 1:
                node += 1
            else:
                node = 0

    @staticmethod
    def get_leaf_nodes(representation: list):
        result = list()
        for node in range(len(representation)):
            child_list = representation[node]
            if len(child_list) == 0:
                result.append(node)
        return result

    @staticmethod
    def get_internal_node(representation: list, root):
        random_start_index = random.randrange(0, len(representation))
        random_walk = random.randrange(0, int(Parameters.random_walk_limit * len(representation)))
        rw_counter = 0
        node = random_start_index
        while node < len(representation):
            if len(representation[node]) != 0 and node != root:
                if rw_counter == random_walk:
                    return node
                rw_counter += 1
            if node != len(representation) - 1:
                node += 1
            else:
                node = 0

    def get_sub_tree_nodes(self, representation: list, fitness, root):
        random_start_index = random.randrange(0, len(representation))
        random_walk = random.randrange(1, max(2, int(Parameters.sub_tree_size_probability * fitness)))
        node = random_start_index
        while node < len(representation):
            if len(representation[node]) == 0:
                leaf_node = node
                break
            if node != len(representation) - 1:
                node += 1
            else:
                node = 0
        current_leaf_node = leaf_node
        for i in range(random_walk):
            parent = self.find_non_root_parent_node(representation, current_leaf_node)
            if parent == root:
                break  # root not is not included
            current_leaf_node = parent
        result = [current_leaf_node]
        result.extend(self.get_node_successors(representation, current_leaf_node))
        return result

    def get_node_successors(self, representation, parent):
        child_list = representation[parent]
        if len(child_list) == 0:
            return list()
        elif len(child_list) == 1:
            child = child_list[0]
            result = list([child])
            result.extend(self.get_node_successors(representation, child_list[0]))
        else:
            result = list()
            for child in child_list:
                result.append(child)
                result.extend(self.get_node_successors(representation, child))
        return result

    def move_node(self, s: Solution, nodes_to_move, node_type):
        representation: list = deepcopy(s.representation)
        if node_type == 'root':
            node_to_move = nodes_to_move[0]
            current_root_child_list = s.representation[s.root]
            representation[node_to_move] = list()
            if len(current_root_child_list) == 1:
                new_root = current_root_child_list[0]
            else:
                new_root = current_root_child_list[random.randrange(0, len(current_root_child_list))]
                for n in current_root_child_list:
                    if n != new_root:
                        representation[new_root].append(n)
            self.place_node(representation, new_root, new_root, node_to_move)
        elif node_type == 'top':
            root_pretenders = list()
            s1 = set(nodes_to_move)
            for i in range(len(nodes_to_move) - 1, -1, -1):
                current_node = nodes_to_move[i]
                current_node_child_list = s.representation[current_node]
                s2 = set(current_node_child_list)
                if len(list(s1.intersection(s2))) == 0:
                    root_pretenders.extend(current_node_child_list)
                else:
                    break
            for n in nodes_to_move:
                representation[n] = list()
            if len(root_pretenders) == 1:
                new_root = root_pretenders[0]
            else:
                new_root = root_pretenders[random.randrange(0, len(root_pretenders))]
                for n in root_pretenders:
                    if n != new_root:
                        representation[new_root].append(n)
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        elif node_type == 'path':
            new_root_assigned = False
            parent_to_link = -1
            if len(nodes_to_move) == len(representation):
                return self.get_initial_solution()
            else:
                for n in range(len(nodes_to_move) - 1):
                    current_parent = nodes_to_move[n]
                    current_child = nodes_to_move[n + 1]
                    child_list = list(representation[current_parent])
                    representation[current_parent] = list()
                    child_list.remove(current_child)
                    if len(child_list) > 0:
                        new_parent = child_list[random.randrange(0, len(child_list))]
                        child_list.remove(new_parent)
                        representation[new_parent].extend(child_list)
                        if not new_root_assigned:
                            new_root = new_parent
                            new_root_assigned = True
                        else:
                            representation[parent_to_link].append(new_parent)
                        parent_to_link = new_parent
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        elif node_type == 'partial_path':
            if len(nodes_to_move) < 2:
                print("new initial solution")
                return self.get_initial_solution()
            new_root = s.root
            parent_to_link = nodes_to_move[0]
            representation[parent_to_link].remove(nodes_to_move[1])
            for n in range(1, len(nodes_to_move) - 1):  # First node does not get removed - it serves as parent
                current_parent = nodes_to_move[n]
                current_child = nodes_to_move[n + 1]
                child_list = list(representation[current_parent])
                representation[current_parent] = list()
                child_list.remove(current_child)
                if len(child_list) > 0:
                    new_parent = child_list[random.randrange(0, len(child_list))]
                    child_list.remove(new_parent)
                    representation[new_parent].extend(child_list)
                    representation[parent_to_link].append(new_parent)
                    parent_to_link = new_parent
            nodes_to_move.pop(0)  # Remove first node
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        elif node_type == 'level':
            new_root = s.root
            for node in nodes_to_move:
                current_node_parent = self.find_non_root_parent_node(s.representation, node)
                representation[current_node_parent].remove(node)
                representation[current_node_parent].extend(representation[node])
                representation[node] = list()
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        elif node_type == 'bottom':
            new_root = s.root
            for node in nodes_to_move:
                current_node_parent = self.find_non_root_parent_node(s.representation, node)
                if (current_node_parent not in nodes_to_move) and (node in representation[current_node_parent]):
                    representation[current_node_parent].remove(node)
            for node in nodes_to_move:
                representation[node] = list()
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        elif node_type == 'leaf':
            node_to_move = nodes_to_move[0]
            new_root = s.root
            current_parent = self.find_non_root_parent_node(representation, node_to_move)
            representation[current_parent].remove(node_to_move)
            self.place_node(representation, new_root, new_root, node_to_move)
        elif node_type == 'leafs':
            new_root = s.root
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node_to_move in nodes_to_move:
                current_parent = self.find_non_root_parent_node(representation, node_to_move)
                representation[current_parent].remove(node_to_move)
                self.place_node(representation, new_root, new_root, node_to_move)
        elif node_type == 'internal':
            node_to_move = nodes_to_move[0]
            new_root = s.root
            node_child_list = s.representation[node_to_move]
            root_child_list = s.representation[s.root]
            if node_to_move in root_child_list:
                parent = s.root
            else:
                parent = self.find_non_root_parent_node(representation, node_to_move)
            representation[parent].remove(node_to_move)
            representation[parent].extend(node_child_list)
            representation[node_to_move] = list()
            self.place_node(representation, new_root, new_root, node_to_move)
        else:  # subtree
            new_root = s.root
            parent_node = nodes_to_move[0]
            parent_of_parent = self.find_non_root_parent_node(representation, parent_node)
            representation[parent_of_parent].remove(parent_node)
            for node in nodes_to_move:
                representation[node] = list()
            nodes_to_move = self.get_ordered_node_list(nodes_to_move)
            for node in nodes_to_move:
                self.place_node(representation, new_root, new_root, node)
        fitness = self.get_fitness(representation, new_root)
        result = Solution(new_root, representation, fitness)
        return result

    def place_node(self, representation, parent, current_node_to_link, node):
        is_internal_node = False
        node_to_link, is_internal_node = self.find_node_to_link(representation, parent, current_node_to_link, node,
                                                                is_internal_node)
        if is_internal_node:
            child_list = representation[node_to_link]
            representation[node_to_link] = list()
            representation[node_to_link].append(node)
            representation[node] = list(child_list)
        else:
            representation[node_to_link].append(node)

    def get_simple_initial_solution(self):
        representation = list()
        for i in range(self.n_nodes):
            lst = list()
            representation.append(lst)
        root = self.number_of_edges_list[0]
        first_child = self.number_of_edges_list[1]
        representation[root].append(first_child)
        for node in range(1, self.n_nodes - 1):
            parent = self.number_of_edges_list[node]
            child = self.number_of_edges_list[node + 1]
            representation[parent].append(child)
        fitness = self.get_fitness(representation, root)
        initial_solution = Solution(root, representation, fitness)
        selected_nodes = self.get_top_nodes(initial_solution)
        node_type = 'top'
        result = self.move_node(initial_solution, selected_nodes, node_type)
        return result

    def get_initial_solution(self):
        representation = list()
        for i in range(self.n_nodes):
            lst = list()
            representation.append(lst)
        root = self.number_of_edges_list[0]
        first_child = self.number_of_edges_list[1]
        representation[root].append(first_child)
        for n in range(2, self.n_nodes, 1):
            node = self.number_of_edges_list[n]
            is_internal_node = False
            node_to_link, is_internal_node = self.find_node_to_link(representation, root, root, node, is_internal_node)
            if is_internal_node:
                child_list = representation[node_to_link]
                representation[node_to_link] = list()
                representation[node_to_link].append(node)
                representation[node] = list(child_list)
            else:
                representation[node_to_link].append(node)
        fitness = self.get_fitness(representation, root)
        result = Solution(root, representation, fitness)
        # if fitness < 11:
        #     print('test')
        return result

    def find_node_to_link(self, representation, parent, current_node_to_link, node, is_internal_node):
        node_to_link = current_node_to_link
        child_list = representation[parent]
        if len(child_list) == 0:
            return node_to_link, is_internal_node
        elif len(child_list) == 1:
            node_to_link_candidate = child_list[0]
            if node in self.adjacency_list[node_to_link_candidate]:
                node_to_link = node_to_link_candidate
            node_to_link, is_internal_node = self.find_node_to_link(representation, node_to_link_candidate,
                                                                    node_to_link, node, is_internal_node)
        else:
            num_paths = 0
            for child in child_list:
                previous_node_to_link = node_to_link
                if node in self.adjacency_list[child]:
                    node_to_link = child
                node_to_link, is_internal_node = self.find_node_to_link(representation, child, node_to_link, node,
                                                                        is_internal_node)
                if previous_node_to_link != node_to_link:
                    num_paths += 1
                    if num_paths == 2:
                        node_to_link = parent
                        is_internal_node = True
                        break
        return node_to_link, is_internal_node

    # def find_node_to_link_non_recursive(self, representation, parent, node, is_internal_node):
    #     node_to_link = parent
    #     child_list = representation[node_to_link]
    #     if len(child_list) == 0:
    #         return node_to_link, is_internal_node
    #     else:
    #         candidate_stack = LifoQueue()
    #         for i in range(len(child_list) - 1, -1, -1):
    #             candidate_stack.put(child_list[i])
    #         while not candidate_stack.empty():
    #             candidate = candidate_stack.get()
    #             if node in self.adjacency_list[candidate]:
    #                 node_to_link = candidate
    #             child_list = representation[candidate]
    #             for i in range(len(child_list) - 1, -1, -1):
    #                 candidate_stack.put(child_list[i])
    #
    #     return node_to_link, is_internal_node

    def get_fitness(self, representation, root):
        result = 1 + self.calculate_fitness(representation, root)
        return result

    def calculate_fitness(self, representation, parent):
        child_list = representation[parent]
        if len(child_list) == 0:
            fitness = 0
        elif len(child_list) == 1:
            fitness = 1 + self.calculate_fitness(representation, child_list[0])
        else:
            max_fitness = -1
            for child in child_list:
                current_fitness = 1 + self.calculate_fitness(representation, child)
                if current_fitness > max_fitness:
                    max_fitness = current_fitness
            fitness = max_fitness
        return fitness

    @staticmethod
    def find_non_root_parent_node(representation: list, node):
        for c in range(len(representation)):
            child_list = representation[c]
            if node in child_list:
                return c
        return -1

    def is_tabu(self, key, iteration):
        if key not in self.tabu_list.keys():
            return False
        if iteration - self.tabu_list[key] <= Parameters.tabu_list_length_probability * self.n_nodes:
            return True
        else:
            return False

    def create_number_of_edges_list(self):
        node_list_with_n_edges = list()
        for i in range(len(self.adjacency_list)):
            node_list_with_n_edges.append([i, len(self.adjacency_list[i])])
        node_list_with_n_edges.sort(key=itemgetter(1),
                                    reverse=Parameters.insert_nodes_in_initial_solution_descending_order)
        current_max_n_edges = node_list_with_n_edges[0][1]
        result = list()
        current_list = list()
        for m in range(len(node_list_with_n_edges)):
            if node_list_with_n_edges[m][1] == current_max_n_edges:
                current_list.append(node_list_with_n_edges[m][0])
            else:
                random.shuffle(current_list)
                result.extend(current_list)
                current_list = list()
                current_list.append(node_list_with_n_edges[m][0])
                current_max_n_edges = node_list_with_n_edges[m][1]
        result.extend(current_list)
        return result

    def get_ordered_node_list(self, node_list: list):
        if Parameters.insert_nodes_in_random_order:
            random.shuffle(node_list)
            return node_list
        node_list_with_n_edges = list()
        for node in node_list:
            node_list_with_n_edges.append([node, len(self.adjacency_list[node])])
        node_list_with_n_edges.sort(key=itemgetter(1), reverse=Parameters.insert_nodes_in_descending_order)
        current_max_n_edges = node_list_with_n_edges[0][1]
        result = list()
        current_list = list()
        for m in range(len(node_list_with_n_edges)):
            if node_list_with_n_edges[m][1] == current_max_n_edges:
                current_list.append(node_list_with_n_edges[m][0])
            else:
                random.shuffle(current_list)
                result.extend(current_list)
                current_list = list()
                current_list.append(node_list_with_n_edges[m][0])
                current_max_n_edges = node_list_with_n_edges[m][1]
        result.extend(current_list)
        return result


def main():
    sys.setrecursionlimit(100000000)
    instance_list = list()
    for i in range(Parameters.start_instance_index, Parameters.end_instance_index, 2):
        instance_name = Parameters.instance_type + "_" + "{0:03}".format(i)
        adjacency_list = Utilities.get_adjacency_list(instance_name)
        ts_alg = TabuSearch(adjacency_list)
        s = ts_alg.ts_algorithm()
        print(instance_name + ": ", s.fitness)
        formatted_solution = Utilities.convert_to_pace_format(s)
        Utilities.save_solution(instance_name, formatted_solution, s.fitness)
    #     instance_list.append(instance_name)
    #     output = pd.DataFrame({'Instance': instance_list, 'Nodes': Utilities.node_list, 'Edges': Utilities.edge_list},
    #                           columns=['Instance', 'Nodes', 'Edges'])
    # output.to_csv('number_of_nodes_and_edges.csv', index=False)


main()
