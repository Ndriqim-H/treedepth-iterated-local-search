
class treedepth:
    file_name = ""
    matrix = {}
    total_points = 0
    def __init__(self,_file_name):
        self.file_name = _file_name
        self.matrix = {}
        self.total_points = 0
        self.read_file()
    #Inicializimi i formes hyrese, pra leximi nga fajlli
    def read_file(self):
        file = open(self.file_name, 'r')
        first_line = file.readline().split(' ')
        self.total_points = int(first_line[2])
        self.fill_matrix()
        total_edge = first_line[3]
        fileRows = filter(None,file.read().split('\n'))
        for row in fileRows:
            element = row.split(' ')
            if int(element[0]) in self.matrix:
                self.matrix[int(element[0])].append(int(element[1]))
            if int(element[1]) in self.matrix:
                self.matrix[int(element[1])].append(int(element[0]))

    def fill_matrix(self):
        for i in range(1,self.total_points+1):
            self.matrix[i] = []



