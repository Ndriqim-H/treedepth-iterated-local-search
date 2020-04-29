# Tabu search parameters
number_of_iterations = 50000
number_of_iterations_with_no_improvement = 150
number_of_tweaks = 10
tabu_list_length_probability = 0.0
fully_random_initial_solution = False
minimal_perturb_intensity = 2
perturbed_solution_deprecation_percentage = 0.75
insert_nodes_in_initial_solution_descending_order = True
insert_nodes_in_random_order = False
insert_nodes_in_descending_order = True
number_of_paths = 15

# Problem related parameters
node_type_selection_probability = {'subtree': 20, 'internal': 0, 'leaf': 0, 'leafs': 0, 'root': 0, 'top': 5,
                                   'bottom': 5, 'level': 0, 'path': 70}
random_walk_limit = 0.1
sub_tree_size_probability = 0.8
top_max_limit_probability = 0.8
bottom_depth_max_limit_probability = 0.05

# Instance selection
instance_type = 'heur'
start_instance_index = 1
end_instance_index = start_instance_index + 1
