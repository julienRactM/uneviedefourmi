# Python file
import json

#Creation de la représenation de la fourmillère

import matplotlib.pyplot as plt
import networkx as nx




class Anthill:
    def __init__(self, file_number = 4):

        # self.all_antshill = json.load("data/antshill.json")
        with open('data/antshill.json', 'r') as file:
            # print(json_data.keys)
            self.json_data = json.load(file)[f'antshill_{file_number}']
            print(self.json_data['Nodes'])

        self.nodes = self.json_data["Nodes"]

        # return json_data


    def visualize(self):
        F = nx.Graph()

        # Adding Nodes first
        for node in self.nodes.keys():
            # print(node)
            F.add_node(node)

        # Then adding edges
        for node in self.nodes.keys():
            for edge in self.nodes[node]:
                F.add_edge(node, edge)

        nx.draw(F, with_labels = True, node_size= 3000)


    def make_paths(self):
        count = 0
        print(self.nodes["Sv"])
        for possibility in self.nodes["Sv"]:
            pass


        # make the loop stop when reaching Sd









if __name__ == "__main__":
    anthill = Anthill(file_number=4)
    # anthill.visualize()
    anthill.make_paths()
