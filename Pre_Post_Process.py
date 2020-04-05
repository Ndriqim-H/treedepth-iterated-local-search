from Solution import Solution


class PrePostProcess:
    file_name = ""
    adjacency_list = {}
    total_points = 0

    def __init__(self, _file_name):
        self.file_name = _file_name
        self.adjacency_list = {}
        self.total_points = 0
        self.read_file()

    def read_file(self):
        file = open(self.file_name, 'r')
        first_line = file.readline().split(' ')
        self.total_points = int(first_line[2])
        self.fill_adjacency_list()
        total_edge = first_line[3]
        fileRows = filter(None, file.read().split('\n'))
        for row in fileRows:
            element = row.split(' ')
            if int(element[0]) in self.adjacency_list:
                self.adjacency_list[int(element[0])].append(int(element[1]))
            if int(element[1]) in self.adjacency_list:
                self.adjacency_list[int(element[1])].append(int(element[0]))

    def fill_adjacency_list(self):
        for i in range(1, self.total_points + 1):
            self.adjacency_list[i] = []

    @staticmethod
    def save_solution(_output_file, s: Solution):
        file = open(_output_file, "w+")
        file.write(str(s.fitness) + "\n")
        for i in range(0, len(s.representation), 1):
            file.write(str(s.representation[i]) + "\n")
        file.close()
