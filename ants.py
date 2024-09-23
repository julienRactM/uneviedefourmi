# Python file
import json
import math
import numpy as np

#Creation de la représenation de la fourmillère

import matplotlib.pyplot as plt
import networkx as nx

from PIL import Image
import io

class Anthill:
    def __init__(self, file_path="data/antshill.json", file_number = 4):

        with open(file_path, 'r') as file: # antshill.json updated_dict.json
            self.json_data = json.load(file)[f'antshill_{file_number}']

        self.nodes = {}
        for node, value in self.json_data["Nodes"].items():
            self.nodes[node] = value[0]

        self.f = self.json_data["f"]
        self.shape = {key: value[1] for key, value in self.json_data["Nodes"].items()}
        self.capacities = {key: value[1] for key, value in self.json_data["Nodes"].items()}

        # return json_data

    def add_new_graph_from_txt(self, file_path):
        with open(f'{file_path}', 'r') as file:
            lines = file.readlines()

        # Parse the content from the text file
        f_value = None
        node_weights = {}
        edges = []
        connected_nodes  = {}

        for line in lines:
            line = line.strip()

            if line.startswith('f='):
                f_value = int(line.split('=')[1].strip())
            elif line.startswith('S') and '-' not in line:
                if '{' in line:
                    parts = line.split('{')
                    node = parts[0].strip()
                    weight = int(parts[1].replace('}', '').strip())
                    node_weights[node] = weight
                else:
                    node = line.strip()
                    node_weights[node] = 1


            if '-' in line:
                if line.split('-')[0].strip() not in connected_nodes:
                    connected_nodes[line.split('-')[0].strip()] = []
                connected_nodes[line.split('-')[0].strip()].append(line.split('-')[1].strip())

                if line.split('-')[1].strip() not in connected_nodes:
                    connected_nodes[line.split('-')[1].strip()] = []
                connected_nodes[line.split('-')[1].strip()].append(line.split('-')[0].strip())
                # needs to use connected now


        with open('data/antshill.json', 'r') as file:
            full_data = json.load(file)

        # Determine the next antshill number
        next_antshill_number = len(full_data) # would be +1 if there were no antshill version 0

        # new entry template
        new_entry = {
            f"antshill_{next_antshill_number}": {
                "f": f_value,
                "Nodes": {}
            }
        }

        # Complete Nodes
        new_entry[f"antshill_{next_antshill_number}"]["Nodes"]['Sv'] = [connected_nodes['Sv'], 1000000000000]

        for node, weight in node_weights.items():
            if weight is not None:
                new_entry[f"antshill_{next_antshill_number}"]["Nodes"][node] = [connected_nodes[node], weight]
            else:
                new_entry[f"antshill_{next_antshill_number}"]["Nodes"][node] = [connected_nodes[node], 1000000000000]  # Default weight

        new_entry[f"antshill_{next_antshill_number}"]["Nodes"]['Sd'] = [connected_nodes['Sd'], 1000000000000]

        # Merge the new entry into the existing dictionary

        full_data.update(new_entry)

        # If you want to save the updated dictionary back to a file (optional step)
        with open('data/updated_dict.json', 'w') as file:
            json.dump(full_data, file, indent=2)

        with open('data/updated_dict.json', 'r') as file:
            self.json_data = json.load(file)[f'antshill_{next_antshill_number}']


        # resetting important values:
        self.nodes = {}
        for node, value in self.json_data["Nodes"].items():
            self.nodes[node] = value[0]

        self.shape = {key: value[1] for key, value in self.json_data["Nodes"].items()}

    def visualize(self):
        F = nx.Graph()

        # Adding Nodes first
        color_map = []
        for node in self.nodes.keys():

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
        print("nodes", self.nodes)
        print(self.all_paths)
        # for path in self.all_paths:
        #     print(" -> ".join(path))

        return self.all_paths

    def init_movement(self, start='Sv', end='Sd'):
        # f is ants count
        self.f = self.json_data['f']
        self.steps = 0

        # attributes self.best_paths and return the best possible paths
        self.path_selection()

        self.nodes_population = dict.fromkeys(self.nodes, 0)
        self.nodes_population['Sv'] = self.f


        # self.movement()

    def movement(self):
        self.best_paths = [self.best_paths] if len(self.best_paths) == 1 else self.best_paths
        for path in [self.best_paths]:
            for i, node in enumerate(path):

                ## Indirect way to check if we're checking Sd or not
                if len(path) >= i+2 and self.nodes_population[node] > 0:
                    next_node_capacity = self.json_data['Nodes'][path[i+1]][1]
                    ### NEED TO ADD A CHECK FOR MULTIPLE PATHS NOT CHEATING OR ATLEAST REVERSE CHECKING THAT IF
                    ### CONTENANCE > MAX CAPACITY REVERT THE CHANGE WITH NODE i-1 getting the reverse increase aftercase


                    available_ants = self.nodes_population[node]
                    available_ants = available_ants if available_ants < next_node_capacity else next_node_capacity

                    self.nodes_population[node] -= available_ants # NEXT SIZE
                    self.nodes_population[path[i+1]] += available_ants
                ### ADD NEXT NODE SIZE



        self.steps +=1
        if self.nodes_population['Sd'] != self.f:
            self.movement()
        else:
            return

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

        self.best_paths = best_paths
        self.best_paths_informations = self.calculate_flow()
        self.best_paths= [entry[0] for entry in self.best_paths_informations]

    def calculate_flow(self):
        temp_paths = []
        for i, path in enumerate(self.best_paths):

            node_flow = []
            for node in path:
                node_flow.append(self.json_data['Nodes'][node][1])

            temp_paths.append([path, np.min(node_flow)])

            # 1 is adjusting for the last node to Sd move
            temp_paths[i].append(math.floor((len(path)-1)/temp_paths[i][1]))


        temp_paths.sort(key=lambda x: x[2])

        return temp_paths

    # Initialiser les positions des fourmis
    def initialize_positions(self, start):
        return {f"f{i+1}": start for i in range(self.f)}

    # Fonction pour afficher tous les plus courts chemins
    def display_all_shortest_paths(self, paths):
        print("Les chemins les plus courts sont :")
        for path in paths:
            print(" -> ".join(path))


    # Fonction pour déplacer les fourmis tout en respectant la capacité des chambres
    def move_ants_with_multiple_paths(self,positions, paths):
        new_positions = positions.copy()

        # Calculer l'occupation des chambres sur tous les chemins
        room_occupancy = {node: list(positions.values()).count(node) for path in paths for node in path}

        for ant, pos in positions.items():
            if pos != paths[0][-1]:  # Si la fourmi n'est pas encore arrivée à destination
                for path in paths:
                    if pos in path and pos != path[-1]:
                        next_pos = path[path.index(pos) + 1]  # Prochaine position dans le chemin
                        # Vérifier si la prochaine chambre peut accueillir plus de fourmis
                        if room_occupancy[next_pos] < self.capacities[next_pos]:  # Respecter la capacité

                            new_positions[ant] = next_pos  # Déplacer la fourmi
                            room_occupancy[pos] -= 1  # Mettre à jour l'occupation de la chambre actuelle
                            room_occupancy[next_pos] += 1  # Mettre à jour l'occupation de la prochaine chambre
                            break  # Dès que la fourmi trouve un chemin valide, on arrête la recherche pour cette fourmi
        return new_positions

    # Fonction pour dessiner le graphe avec l'occupation des chambres
    def draw_graph_with_occupancy(self, G, capacities, positions, step, seed=12):
        plt.figure(figsize=(10, 6))

        plt.gca().set_facecolor('#151b23')

        # Dessiner le graphe avec une disposition déterministe
        pos = nx.spring_layout(G, seed=seed, k=1)  # Positionnement des nœuds avec une graine pour la reproductibilité
        color_map = ["#548CAC"] + ["#7edb32"]*(len(pos)-2) + ["#1ea4d9"]

        # Dessiner le graphe avec une disposition déterministe
        pos = nx.spring_layout(G, seed=seed)  # Positionnement des nœuds avec une graine pour la reproductibilité
        nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=2300  , font_size=16, font_weight='bold', edge_color='gray')
        # Changing value temporarily for img
        capacities["Sv"] = "∞"
        capacities["Sd"] = "∞"

        # Annoter les capacités des chambres
        labels = {node: f"{capacities[node]}\n\n({list(positions.values()).count(node)})" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=14, font_color='black')

        plt.title(f"Étape {step}: Occupation des chambres")

        # Sauvegarder la figure en tant qu'image dans un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()


        capacities["Sv"] = float('inf')
        capacities["Sd"] = float('inf')

        return Image.open(buf)

    # Fonction pour simuler les déplacements des fourmis avec plusieurs chemins possibles
    def simulate_ants_movement_with_multiple_paths(self, start, end):
        # 1. Calculer et afficher tous les chemins les plus courts
        paths = self.best_paths
        print(paths)
        self.display_all_shortest_paths(paths)
        capacities = self.capacities

        # 2. Simuler le déplacement des fourmis sur plusieurs chemins
        positions = self.initialize_positions(start)  # Initialiser les positions des fourmis
        step = 1

        images = []
        while any(pos != end for pos in positions.values()):  # Tant que toutes les fourmis ne sont pas arrivées

            # Déplacer les fourmis tout en respectant la capacité sur plusieurs chemins
            positions = self.move_ants_with_multiple_paths(positions, paths)

            print(f"\n+++ Étape {step} +++")
            for ant, pos in positions.items():
                print(f"{ant} est dans {pos}")


            # Ajouter une capacité infinie pour la chambre de destination (Sd)
            capacities["Sd"] = float('inf')


            G = nx.Graph()
            for node, neighbors in self.nodes.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            # Dessiner le graphe avec l'occupation des chambres et sauvegarder l'image
            img = self.draw_graph_with_occupancy(G, capacities, positions, step)
            images.append(img)

            step += 1

        # Dernière étape où toutes les fourmis sont arrivées
        print(f"\n+++ Étape {step} +++")
        for ant, pos in positions.items():
            print(f"{ant} est arrivée")

        # Dessiner le graphe final et sauvegarder l'image
        img = self.draw_graph_with_occupancy(G, capacities, positions, step)
        images.append(img)

        # Créer le GIF à partir des images
        images[0].save('antshill.gif', save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0)


# Extraire les nœuds et les capacités



# Exemple : Simuler le déplacement de 10 fourmis de 'Sv' à 'Sd' avec capacités sur plusieurs chemins



if __name__ == "__main__":
    anthill = Anthill(file_number=4)
    anthill.init_movement()
    anthill.simulate_ants_movement_with_multiple_paths("Sv", "Sd")

    # print("Les chemins sont:", anthill.best_paths)
    # print("Nombre de fourmis:", anthill.f)
    # print("Connexions des chambres:", anthill.nodes)
    # print("Capacités des chambres:", anthill.capacities)








    # print(anthill.shape)
    anthill.add_new_graph_from_txt("fichiers txt/fourmiliere_sept.txt")
    # print(anthill.json_data)
    # anthill.init_movement()
    # print("best path found:", anthill.best_paths[0])
