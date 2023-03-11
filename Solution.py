class IteratedSearch:
    def __init__(self) -> None:
        self.adjacency_list = [[1, 4, 5], [0, 2, 6], [1, 3, 7], [2, 4, 8], [0, 3, 9], [0, 7, 8], [1, 8, 9], [2, 5, 9], [3, 5, 6], [4, 6, 7]]
        # self.adjacency_list = {0: [6, 1], 1: [4, 3, 6, 2, 0, 12, 15], 
        # 2: [8, 6, 5, 10, 7, 11, 13, 15, 1], 3: [8, 6, 7, 11, 1, 9, 13, 10, 5], 
        # 4: [8, 5, 1, 7, 11, 10, 9, 6, 13], 5: [4, 8, 3, 6, 16, 13, 9, 2, 10, 7, 15], 
        # 6: [4, 8, 3, 11, 10, 2, 5, 9, 13, 1, 12, 0, 7], 7: [4, 8, 3, 6, 5, 9, 10, 13, 14, 2], 
        # 8: [4, 5, 7, 3, 10, 13, 9, 2, 6, 11], 9: [4, 8, 3, 6, 5, 10, 7, 15, 13], 
        # 10: [4, 8, 3, 6, 5, 9, 2, 13, 7, 11], 11: [4, 8, 3, 6, 10, 2], 12: [6, 1], 
        # 13: [4, 8, 3, 6, 5, 9, 10, 7, 2, 15], 14: [7], 15: [5, 9, 2, 13, 1], 16: [5]}


    def find_node_to_link(self, representation, parent, current_node_to_link, node, is_internal_node):
            node_to_link = current_node_to_link
            child_list = representation[parent]
            if len(child_list) == 0:
                return node_to_link, is_internal_node
            elif len(child_list) == 1:
                node_to_link_candidate = child_list[0]
                if node in self.adjacency_list[node_to_link_candidate]:
                    node_to_link = node_to_link_candidate
                node_to_link, is_internal_node = self.find_node_to_link(representation, node_to_link_candidate,
                                                                        node_to_link, node, is_internal_node)
            else:
                num_paths = 0
                for child in child_list:
                    previous_node_to_link = node_to_link
                    if node in self.adjacency_list[child]:
                        node_to_link = child
                    node_to_link, is_internal_node = self.find_node_to_link(representation, child, node_to_link, node,
                                                                            is_internal_node)
                    if previous_node_to_link != node_to_link:
                        num_paths += 1
                        if num_paths == 2:
                            node_to_link = parent
                            is_internal_node = True
                            break
            return node_to_link, is_internal_node

    

    def find_node_to_link2(self, representation, root, node):

        neighbors = self.adjacency_list[node]
        neighbors_in_representation = []
        parents_of_neighbors = []
        
        for i, n in enumerate(representation):
            for neighbor in neighbors:
                if(neighbor in n):
                    neighbors_in_representation.append(neighbor)
                    parents_of_neighbors.append(i)

        if(len(neighbors_in_representation) == 0):
            return root, False
        elif(len(neighbors_in_representation) == 1):
            return neighbors_in_representation[0], False

        else:
            highest_parent = self.find_highest_parent(parents_of_neighbors, root, representation)
            
            while True:
                if(highest_parent == root):
                    return root, True

                if(self.valid_parent(highest_parent, representation, neighbors_in_representation)):
                    return highest_parent, True
                else:
                    highest_parent = self.find_parent_in_representation(root, highest_parent, representation)
            


            return highest_parent, True
            
            return parents_of_neighbors[0], True

        return True
        
    def find_highest_parent(self, parents, root, representation):
        queue = [root]
        while len(queue) > 0:
            curr_node = queue.pop(0)
            if(curr_node in parents):
                return curr_node
            for node in representation[curr_node]:
                queue.append(node)

        return root

    def find_parent_in_representation(self, root, node, representation):
        queue = [root]
        while(len(queue) > 0):
            curr_node = queue.pop(0)
            if(node in representation[curr_node]):
                return curr_node

            for n in representation[curr_node]:
                queue.append(n)

        return root

    def valid_parent(self, parent, representation, neighbors_in_representation):
        # visited = [False for i in range(len(representation))]
        visited = []
        
        stack = []
        stack.append(parent)
        count = 0
        while len(stack) > 0:
            curr_node = stack.pop()
            
            if(curr_node not in visited):
                visited.append(curr_node)
            
            for node in representation[curr_node]:
                if(node not in visited):
                    stack.append(node)
                
        if(len(representation[curr_node]) == 0):
                for v in visited:
                    if(v in neighbors_in_representation):
                        count += 1

                if(count != len(neighbors_in_representation)):
                    return False
                else:
                    return True
        return False

test = IteratedSearch()    
representation = [[1], [6,2], [3], [], [], [], [9], [], [], []]
node = 4
x = test.find_parent_in_representation(0,9,representation)
test.valid_parent(1, representation, [3, 9])

node_to_link2, isinternal_node2 =  test.find_node_to_link2(representation, 0, node)
if isinternal_node2:
    # child_list = representation[node_to_link1]
    # representation[node_to_link1] = list()
    # representation[node_to_link1].append(node)
    # representation[node] = list(child_list)

    # Testing case
    child_list = representation[node_to_link2]
    representation[node_to_link2] = list()
    representation[node_to_link2].append(node)
    representation[node] = list(child_list)
else:
    # representation[node_to_link1].append(node)
    representation[node_to_link2].append(node)


print("Hweasd")

representation = [[]]*17
representation[0] = [5]

representation = [[], [], [], [], [], [], [5], [], [], [], [], [], [], [], [], [], []]
representation1 = representation.copy()
root = 6

node = 2
n_nodes = 17
# number_of_edges_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
number_of_edges_list = [6, 5, 8, 7, 10, 13, 2, 9, 3, 4, 1, 11, 15, 12, 0, 14, 16]

for n in range(2, n_nodes, 1):
    node = number_of_edges_list[n]
    is_internal_node = False
    # node_to_link1, is_internal_node1 = test.find_node_to_link(representation, root, root, node, is_internal_node)
    node_to_link2, isinternal_node2 =  test.find_node_to_link2(representation1, root, node)
    if isinternal_node2:
        # child_list = representation[node_to_link1]
        # representation[node_to_link1] = list()
        # representation[node_to_link1].append(node)
        # representation[node] = list(child_list)

        # Testing case
        child_list = representation1[node_to_link2]
        representation1[node_to_link2] = list()
        representation1[node_to_link2].append(node)
        representation1[node] = list(child_list)
    else:
        # representation[node_to_link1].append(node)
        representation1[node_to_link2].append(node)

    
print("Hello")
    
