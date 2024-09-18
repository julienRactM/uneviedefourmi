# Python file
import json

#Creation de la représenation de la fourmillère

import matplotlib.pyplot as plt
import networkx as nx

class Anthill:
    def __init__(self, file_number = 4):

        # self.all_antshill = json.load("data/antshill.json")
        with open('data/antshill.json', 'r') as file:
            self.json_data = json.load(file)[f'antshill_{file_number}']
            # print(self.json_data['Nodes'])

        self.nodes = {}
        for node, value in self.json_data["Nodes"].items():
            self.nodes[node] = value[0]


        # return json_data

    def visualize(self):
        F = nx.Graph()

        # Adding Nodes first
        color_map = []
        for node in self.nodes.keys():
            print(node)

            F.add_node(node)

            if node == "Sv":
                color_map.append('#930ac9')
            elif node == "Sd":
                color_map.append('#7edb32')
            else :
                color_map.append('#1ea4d9')

        # Then adding edges
        for node in self.nodes.keys():
            for edge in self.nodes[node]:
                F.add_edge(node, edge)


    ### Fixed position makes questionable graphs, can be used for presentation thought.
                # Generate positions using spring layout
        # pos = nx.spring_layout(F)  # This generates default positions

        # # Manually set "Sv" to the far left (e.g., x=-1.0)
        # pos["Sv"] = [-1.0, 0.0]  # Move "Sv" to the left side

        # # Optionally adjust the layout of other nodes if needed
        # pos["Sd"] = [1.0, 0.0]  # You can adjust "Sd" or other nodes as well

        nx.draw(F, node_color=color_map, with_labels = True, node_size= 1200) # pos
        plt.show()

    def find_all_paths(self, start='Sv', end='Sd'):
        graph = self.nodes.copy()
        def dfs(current_node, path):
            if current_node == end:
                self.all_paths.append(path.copy())
                return
            for neighbor in graph.get(current_node, []):
                if neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, path)
                    path.pop()

        self.all_paths = []
        dfs(start, [start])
        # for path in self.all_paths:
        #     print(" -> ".join(path))

        return self.all_paths

    def init_movement(self, start='Sv', end='Sd'):
        # f is ants count
        self.f = self.json_data['f']
        self.steps = 0


        # attributes self.best_paths list of list to the Instance
        self.path_selection()

        self.nodes_population = dict.fromkeys(self.nodes, 0)
        self.nodes_population['Sv'] = self.f

        # graph = self.nodes

        while self.nodes_population['Sd'] != self.f:
            self.movement()

    def movement(self):
        print(self.nodes_population)
        for path in [self.best_paths]:
            for i, node in enumerate(path):
                print(path)

                self.nodes_population[node] -=1
                self.nodes_population[path[i+1]] +=1


        self.steps +=1
        return




        # test = self.json_data.get("shape", [{}])[0]
        # print(test)

    def path_selection(self):
        all_paths = self.find_all_paths()
        all_paths = sorted(all_paths, key=len)  # Sort paths by length (shortest first)

        all_paths_score = []

        for path in all_paths:
            score = 0
            for node in path:
                if self.json_data["Nodes"][node][1] != 1:
                    score += self.json_data["Nodes"][node][1]
            all_paths_score.append(score)

        temp_all_paths = []
        while len(all_paths)>1:
            all_same_len_paths = [path for path in all_paths if len(path) == len(all_paths[0])]

            # Get the indices of these paths in the original list
            indices_of_same_len_paths = [i for i, path in enumerate(all_paths) if len(path) == len(all_paths[0])]
            all_same_len_scores = [all_paths_score[i] for i in indices_of_same_len_paths]

            if len(all_same_len_paths) > 1 and all_same_len_scores[0] < max(all_same_len_scores):

                max_index = all_paths_score.index(max(all_same_len_scores))

                temp_all_paths.append(all_same_len_paths[max_index])
                all_paths_score.pop(max_index)
                all_paths.pop(max_index)

            else:
                temp_all_paths.append(all_paths[0])
                all_paths_score.pop(0)
                all_paths.pop(0)

        # adding last remaining path separately
        temp_all_paths.append(all_paths[0])
        best_paths = temp_all_paths


        # only taking into account all the shortest paths and the one longer by one move at the moment
        # best_paths = [path for path in all_paths[1:] if len(path)<=len(all_paths[0])+1]

        for path in best_paths:
            print(" -> ".join(path))

        self.best_paths = best_paths[0] # [0:5]



    def make_brute_path(self):
        count = 0

        # En gros

        # make the loop stop when reaching Sd

    def random_path(self, pos='Sv'):
        pass
        # print(self.nodes)
        # available_nodes = self.nodes

        # while available_nodes:

        #     if len(self.nodes[pos]) > 1:
        #         for possibility in self.nodes[pos]: # add random
        #             available_nodes.remove(possibility)
        #     else:
        #         pass


if __name__ == "__main__":
    anthill = Anthill(file_number=5)
    # anthill.visualize()
    # anthill.make_paths()
    # anthill.random_path()
    anthill.init_movement()
