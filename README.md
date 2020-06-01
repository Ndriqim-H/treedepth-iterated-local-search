# treedepth-iterated-local-search

Short description

This is a solver for the tree depth problem, which the topic of PACE 2020 competition. The solver is based on the iterated local search algorithm, whilst it utilizes also features from tabu search methauristc. It is developed by using Python3 and interpreted through Anaconda 3 distribution.

Dependencies

•	Operator library (operator — Standard operators as functions - https://docs.python.org/3/library/operator.html#module-operator)

•	Queue library (queue — A synchronized queue class - https://docs.python.org/3/library/queue.html)

Installation and running using Python 2.7

-Download the script ils_solver.py

-In the folder, where the solver is saved, create a new folder named 'instances' and place all private (and/or public) instances of the tree-depth problem 

-In the folder, where the solver is saved, create a new folder named ‘solutions’ where the solutions will be saved

-Run the algorithm in of the three modes as described below:

•	Run a single instance (e.g. instance  exact_001.gr) by writing this command: python ils_solver.py --exact_001.gr

•	Run all private instances by writing this command: python ils_solver.py --private

•	Run all public instances by writing this command: python ils_solver.py --public

Note that if you send the SIGINT signal to the solver, when the algorithm is run to solve all private/public instances, the solution to the current instance will be saved to the disk, and then, the solver will proceed with next instance, until it solves all the instances (i.e. the instance exact_200.gr for private data set, or  the instance exact_199.gr for the public data set)
