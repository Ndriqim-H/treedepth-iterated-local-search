from HillClimbing import hill_climbing
from Treedepth import treedepth
from SignalHandler import signal_handler

if __name__ == '__main__':
    signal_handler = signal_handler()
    tree = treedepth("public/heur_001.gr")
    ##alg = hill_climbing(tree.matrix,tree.total_points)
    tabu_search_algorithm = tabu_search(tree.matrix)
    tabu_search_algorithm.ts_algorithm()
    #while not signal_handler.finish_proccess:
    #  alg.specific_move()
    #alg.calculate_full_fitness(alg.solution)
    #alg.save_solution("heur_001_solution.out")
