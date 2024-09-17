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


    def make_brute_path(self):
        count = 0


        # En gros

        # make the loop stop when reaching Sd









if __name__ == "__main__":
    anthill = Anthill(file_number=4)
    # anthill.visualize()
    anthill.make_paths()
