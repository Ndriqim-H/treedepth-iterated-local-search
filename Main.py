from HillClimbing import hill_climbing
from Pre_Post_Process import PrePostProcess
from SignalHandler import signal_handler
from IteratedLocalSearch import TabuSearch
from Solution import Solution
import Parameters

if __name__ == '__main__':
    signal_handler = signal_handler()
    pre_post = PrePostProcess("instances/" + Parameters.instance_name + ".gr")
    tabu_search_algorithm = TabuSearch(pre_post.adjacency_list)
    best: Solution = tabu_search_algorithm.ts_algorithm()
    pre_post.save_solution("solutions/" + Parameters.instance_name + "_solution.out", best)
