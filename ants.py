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

        self.nodes = self.json_data["Nodes"]

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
        for path in self.all_paths:
            print(" -> ".join(path))

        return self.all_paths

    def init_movement(self, start='Sv', end='Sd'):
        # shape is the amount of ants a node can contain
        self.shape = self.json_data["shape"]
        # f is ants count
        self.f = self.json_data['f']


        self.best_paths = self.path_selection()

        self.nodes_population = dict.fromkeys(self.nodes, 0)
        self.nodes_population['Sv'] = self.f

        graph = self.nodes

        # while self.nodes_population['Sd'] != self.f:
        #     self.movement()

    def movement(self):
        pass
        # for path in enumerate(self.best_paths):
        #     # print(path)
        #     path


        # test = self.json_data.get("shape", [{}])[0]
        # print(test)

    def path_selection(self):
        all_paths = self.find_all_paths()
        all_paths = sorted(all_paths, key=len)  # Sort paths by length (shortest first)

        all_paths_score = []

        for path in all_paths:
            score = 0
            # score += size for larger_rooms, size in self.shape.keys()
            for node in path:
                print(node)
                print(self.shape)
                if node in self.shape.keys():
                    score += self.shape[node]
            all_paths_score.append(score)

        print(all_paths_score)

        # only taking into account all the shortest paths and the one longer by one move at the moment
        # best_paths = [path for path in all_paths[1:] if len(path)<=len(all_paths[0])+1]

        # to remove at some point
        best_paths = all_paths[0]


    def make_brute_path(self):
        count = 0

        # En gros

        # make the loop stop when reaching Sd

    def random_path(self, pos='Sv'):

        print(self.nodes)
        available_nodes = self.nodes

        while available_nodes:

            if len(self.nodes[pos]) > 1:
                for possibility in self.nodes[pos]: # add random
                    available_nodes.remove(possibility)
            else:
                pass


if __name__ == "__main__":
    anthill = Anthill(file_number=5)
    # anthill.visualize()
    # anthill.make_paths()
    # anthill.random_path()
    anthill.init_movement()
