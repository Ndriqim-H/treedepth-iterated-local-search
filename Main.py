from HillClimbing import hill_climbing
from Pre_Post_Process import PrePostProcess
from SignalHandler import SignalHandler
from ils_solver import IteratedLocalSearch
from Solution import Solution
import Parameters

if __name__ == '__main__':
    signal_handler = SignalHandler()
    pre_post = PrePostProcess("instances/" + Parameters.instance_name + ".gr")
    tabu_search_algorithm = IteratedLocalSearch(pre_post.adjacency_list)
    best: Solution = tabu_search_algorithm.ils_algorithm()
    pre_post.save_solution("solutions/" + Parameters.instance_name + "_solution.out", best)
