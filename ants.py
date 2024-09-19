import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re


class Antnest:
    """ nombre de fourmis, nbre de salles, liste de salles, tunnels,
        taille salle, nom salle, 
    
    """
    def __init__(self, filename):
            
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        lines = [ elmt.strip() for elmt in lines]
        self.nbF = self.get_ants(lines)
        # self.nbS= nbS
        self.rooms= self.get_rooms(lines)
        self.tunnels= self.get_tunnels(lines)
       
    def get_ants(self, lines):
        for line in lines:
            if(re.findall('^[Ff]=', line)):
                nbF = line.split('=')[1]
        return nbF

    def get_rooms(self, lines):
        """ Retourne une liste d'objets de type salle """
       
        rooms=[]
        for line in lines:       
            if (re.findall('^S.*}$|^S[0-9]+$', line)):
                name = line.split()[0]
                if len(line.split()) > 1:
                    size= line.split()[2]
                    salle  = Salle(name, size) 

                else:
                    salle = Salle(name)
                    
                
                rooms.append(salle)
        return rooms

    def get_tunnels(self,lines):
        """Retourne la liste des ponts entre les salles"""
        tunnels=[]
        for line in lines:  
            x = re.findall('^S.*-.*S.*$', line)
            if x:
                
                tunnels.append(line)
        return tunnels
        
    def createGraph(self):
        """Gènère les graphes des fourmilières"""
        G = nx.Graph()

        for room in self.rooms:
            G.add_node(room.name)

        for edge in self.tunnels:
            edge = edge.split(' - ')
            G.add_edge(edge[0],edge[1])

        nx.draw(G, with_labels=True)
        plt.show()
        
        def moving_ants(self):
            """ Returns the movement stages of the ants """
            f = 1
            etape1 = []
            etape2 = []
            #t= re.findall('^Sv.*', self.tunnels)
            t = [tunnel for tunnel in self.tunnels if tunnel.startswith('Sv')]
            #print(t)
            for tunnel in t:
                #if tunnel.startswith('Sv'):
                destination = tunnel.split(' - ')[1]
                size = [salle.size for salle in self.rooms if salle.name == destination][0]
                for i in range(1, size + 1):
                    step = 'f' + str(f )
                    step= step + ' - ' + tunnel
                    f +=1
                    etape1.append(step)
        
        
       
    

                
class Salle:
    """ Defines the name and size of the room """
    def __init__(self , name, size = 1):
        self.size = int(size)
        self.name =name
        
      
ant1 = Antnest('fourmiliere_quatre.txt')
ant1.createGraph()

print("Number of ants : ", ant1.nbF)
for room in ant1.rooms:
    print(room.name, room.size)
    print(ant1.tunnels)





   


   





        
       
            





    







