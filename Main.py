from HillClimbing import hill_climbing
from Treedepth import treedepth
from SignalHandler import signal_handler

if __name__ == '__main__':
  signal_handler = signal_handler()
  tree = treedepth("public/heur_001.gr")
  alg = hill_climbing(tree.matrix,tree.total_points)
  while not signal_handler.finish_proccess:
      print()
      #to do
      #apply hill climbing algorithm to improve solution / until signal is not sent

  print(alg.solution)
  alg.save_results("file_name.out")


