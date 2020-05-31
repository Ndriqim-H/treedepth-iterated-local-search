# treedepth-iterated-local-search

Short description
This is a solver for the tree depth problem, which the topic of PACE 2020 competition. The solver is based on the iterated local search algorighm, whilst it utilizes also features from tabu search methauristc.It is developed by using Python3 and intepreted through Anaconda3 distribution.

Dependencies

•	Operator library (operator — Standard operators as functions - https://docs.python.org/3/library/operator.html#module-operator)

•	Queue library (queue — A synchronized queue class - https://docs.python.org/3/library/queue.html)


Installatin and running
Download the script ils_solver.py
In the folder, where the solver is saved, create a new folder named 'instances' and place all private (and/or) public instances of the tree-depth problem 
In the folder, where the solver is saved, create a new folder named ‘solutions’ where the solutions will be saved
Open the console of a Python3 interpreter (example Anaconda Prompt (Anaconda3))
Run the algorithm in of the three modes as described below:
•	Run a single instance by writing this command: ils_solver.py --exact_001.gr
•	Run all private instances by writing this command: ils_solver.py --private
•	Run all public instances by writing this command: ils_solver.py --public 
