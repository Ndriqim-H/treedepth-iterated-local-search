import random
import copy

class hill_climbing:
    input_form = {}
    size = 0
    solution = []
    root = -1
    fitnes = 0

    def __init__(self,_input_form, _size):
        self.input_form = _input_form
        self.size = _size
        self.root = self.get_root()
        self.initialize_solution()
        self.calculate_full_fitness()

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
        self.solution = [-1] * self.size
        self.solution[self.root-1] = 0
        random_array.remove(self.root)
        random.shuffle(random_array)
        _parent = copy.copy(self.root)
        while len(random_array) != 0:
            tmp_var = random.choice(random_array)
            while tmp_var == _parent - 1:
                tmp_var = random.choice(random_array)
            self.solution[tmp_var-1] = _parent
            _parent = copy.copy(tmp_var)
            random_array.remove(tmp_var)

        return 0

    def save_solution(self,_output_file):
        file = open(_output_file, "w+")
        file.write(str(self.fitnes) + "\n")
        for i in range(0, len(self.solution), 1):
            file.write(str(self.solution[i]) + "\n")
        file.close()

    def move(self):
        tmp_array = list(range(1, len(self.solution)+1))
        leafs = list(set(tmp_array) - set(self.solution))
        leafs = list(set(leafs) - set([self.root]))
        x = random.choice(leafs)
        y = random.randint(0,len(self.solution))
        while x == y:
            y = random.randint(0,len(self.solution))
        if self.is_legal_move(x,y):
            self.solution[x-1] = copy.copy(y)
            print("Legal Move")
            self.calculate_full_fitness()
            print("Fitnes: ",self.fitnes)
        return False

    def is_legal_move(self,_point,_parent):
        all_node_parent = self.find_all_parents(_point)
        all_parent_parent = self.find_all_parents_include(_parent)
        for pp in all_parent_parent:
            if pp in all_node_parent:
                all_node_parent.remove(pp)

        for old_parent in all_node_parent:
            if _point in self.input_form[old_parent]:
                return False
        return True

    def specific_move(self):
        tmp_array = list(range(1, len(self.solution)+1))
        leafs = list(set(tmp_array) - set(self.solution))
        leafs = list(set(leafs) - set([self.root]))
        #TO DO
        #zgjedhe nje leaf random nga leafs
        #zgjedhje nje prind random nga prinderit ne tabelen kryesore
        #if self.is_legal_move(leaf, new_parent):
        #for leaf in leafs:
        #    if self.is_legal_move_leaf(leaf):
        #        print("YESSSSSSSSS")

    def is_legal_move_leaf(self,_leaf):
        tmp_value = 0
        all_leaf_parents = self.find_all_parents(_leaf)
        for _parent in all_leaf_parents:
            tmp_value = tmp_value + 1
            if _leaf in self.input_form[_parent]:
                self.solution[_leaf-1] = copy.copy(_parent)
                return True
            if _parent == 0:
                return True
        return False

    def calculate_full_fitness(self):
        tmp_array = list(range(1, len(self.solution)+1))
        leafs = list(set(tmp_array) - set(self.solution))
        leafs = list(set(leafs) - set([self.root]))
        all_fitnes_values = []
        for leaf in leafs:
            _value = 2
            _parent = self.solution[leaf-1]
            while self.solution[_parent-1] != 0:
                _value = _value + 1
                _parent = self.solution[_parent-1]
            all_fitnes_values.append(_value)
        self.fitnes = max(all_fitnes_values)

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

    def find_all_children_include(self,_parent):
        all_children = [_parent]
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

    def find_all_parents(self,_node):
        _parents = []

        _parent = self.solution[_node-1]
        if(self.solution[_node-1]!=0):
            _parents.append(_parent)
        while self.solution[_parent-1] != 0:
            _parent = self.solution[_parent-1]
            _parents.append(_parent)
        return _parents

    def find_all_parents_include(self,_node):
        _parents = [_node]
        _parent = self.solution[_node-1]
        _parents.append(_parent)
        while self.solution[_parent-1] != 0:
            _parent = self.solution[_parent-1]
            _parents.append(_parent)
        return _parents

    def find_all_old_parent(self,_node,_new_parent):
        _parents = []
        _parent = self.solution[_node-1]
        _parents.append(_parent)
        while self.solution[_parent-1] != 0 and self.solution[_parent-1] != _new_parent:
            _parent = self.solution[_parent-1]
            _parents.append(_parent)
        return _parents
