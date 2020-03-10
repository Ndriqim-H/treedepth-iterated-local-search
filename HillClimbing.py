import random
import copy

class hill_climbing:
    input_form = {}
    #in this dictionary we are going to save all chilcren of all parents
    help_form = {}
    size = 0
    solution = []
    root = -1
    fitness = 0

    def __init__(self,_input_form, _size):
        self.input_form = _input_form
        self.size = _size
        self.root = self.get_root()
        self.initialize_solution()

    def get_root(self):
        root = 1
        len_root = len(self.input_form[root])
        for i in self.input_form:
            if len(self.input_form[i]) >= len_root:
                root = i
                len_root = len(self.input_form[i])
        return root

    def initialize_help_form(self):
        for i in range(1,self.size+1):
            self.help_form[i] = []
        self.help_form[self.root] = [-1]

    def initialize_solution(self):
        random_array = random.sample(range(1, self.size+1), self.size)
        self.solution = [-1] * 100
        self.solution[self.root-1] = 0
        random_array.remove(self.root)
        random.shuffle(random_array)
        _parent = copy.copy(self.root)
        for i in range(0,len(random_array)):
            self.solution[random_array[i]-1] = copy.copy(_parent)
            _parent = copy.copy(random_array[i])
        return 0

    def get_random_item_array(self,i,array):
        item = -1
        for tmp in range(0,len(array)):
            if array[tmp] != i  and array[tmp] != self.leaf:
                item = array[tmp]
                array.pop(tmp)
                return item, array
        print("Error found!")

    def save_solution(self,_output_file):
        file = open(_output_file, "w+")
        file.write(str(len(self.actualSolution)) + "\n")
        for i in range(0, len(self.solution), 1):
            file.write(str(self.solution[i]) + "\n")
        file.close()

    def move(self):
        x = random.randint(0,len(self.solution))
        y = random.randint(0,len(self.solution))
        while x == y + 1 or self.solution[x-1]==0:
            x = random.randint(0,len(self.solution))

        if self.is_legal_move(x,y):
            #make move
            return True
        return False

    def is_legal_move(self,_point,_parent):

        return True

    def calculate_full_fitness(self,_solution):
        tmp_array = list(range(1, 101))
        leafs = list(set(tmp_array) - set(_solution))
        leafs = list(set(leafs) - set([self.root]))
        all_fitness_values = []
        for leaf in leafs:
            _value = 1
            _parent = _solution[leaf-1]
            while  _solution[_parent-1] != 0:
                _value = _value + 1
                _parent = _solution[_parent-1]
            all_fitness_values.append(_value)
        self.fitness = max(all_fitness_values)

    def calculate_fitness(self,_x,_y):
        return 0

    def find_all_children(self,_parent):
        all_children = []
        tmp_children = self.get_children_of_parent(_parent)
        for children in tmp_children:
            all_children.append(children)
            next_children = self.get_children_of_parent(children)
            for _next_children in next_children:
                tmp_children.append(_next_children)
        return all_children

    def get_children_of_parent(self,_parent):
        all_children = []
        for i in range(0,len(self.solution)):
            if _parent == self.solution[i]:
                all_children.append(i+1)
        return all_children

    def find_all_parents(self,_solution,_node):
        _parents = []
        _parent = _solution[_node-1]
        _parents.append(_parent)
        while _solution[_parent-1] != 0:
            _parent = _solution[_parent-1]
            _parents.append(_parent)
        return _parents
