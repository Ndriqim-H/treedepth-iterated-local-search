import random
import copy

class solution:
    def __init__(self, _input_form ):
        #self.representation = [-1] * _n_nodes
        self.input_form = _input_form
        self.fitness = len(_input_form)
        self.root = self.get_root()
        self.representation = self.get_initial_solution( len(_input_form))

    def get_initial_solution(self, _n_nodes: int):
        random_array = random.sample(range(1, _n_nodes + 1), _n_nodes)
        result = [-1] * _n_nodes
        result[self.root - 1] = 0
        random_array.remove(self.root)
        random.shuffle(random_array)
        _parent = copy.copy(self.root)
        for i in range(0, len(random_array)):
            result[random_array[i] - 1] = copy.copy(_parent)
            _parent = copy.copy(random_array[i])
        return result

    def get_root(self):
        root = 1
        len_root = len(self.input_form[root])
        for i in self.input_form:
            if len(self.input_form[i]) >= len_root:
                root = i
                len_root = len(self.input_form[i])
        return root

    #implementimi i llogaritjes se fitnesit
    def calculate_fitness(self):
        tmp_array = list(range(1, 101))
        leafs = list(set(tmp_array) - set(self.representation))
        leafs = list(set(leafs) - set([self.root]))
        all_fitness_values = []
        for leaf in leafs:
            _value = 1
            _parent = self.representation[leaf-1]
            while self.representation[_parent-1] != 0:
                _value = _value + 1
                _parent = self.representation[_parent-1]
            all_fitness_values.append(_value)
        self.fitness = max(all_fitness_values)

    def save_solution(self,_output_file):
        self.calculate_fitness()
        file = open(_output_file, "w+")
        file.write(str(self.fitness) + "\n")
        for i in range(0, len(self.representation), 1):
            file.write(str(self.representation[i]) + "\n")
        file.close()


