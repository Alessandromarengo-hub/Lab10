import networkx as nx
from database.dao import DAO

class Model:
   def __init__(self):
       self._nodes = None
       self._edges = None
       self.G = nx.Graph()


   def pulizia(self):
       self.G.clear()


   def costruisci_grafo(self, threshold):
       """
       Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
       guadagno medio per spedizione >= threshold (euro)
       """
       lista_meritevoli = DAO().grafo_filtrato(threshold)
       for elemento in lista_meritevoli:
           self.G.add_node(elemento.id_hub1)
           self.G.add_node(elemento.id_hub2)


       for elemento in lista_meritevoli:
           self.G.add_edge(elemento.id_hub1, elemento.id_hub2, weight = elemento.valore)




   def get_num_edges(self):
       return self.G.number_of_edges()
       """
       Restituisce il numero di Tratte (edges) del grafo
       :return: numero di edges del grafo
       """




   def get_num_nodes(self):
       return self.G.number_of_nodes()
       """
       Restituisce il numero di Hub (nodi) del grafo
       :return: numero di nodi del grafo
       """




   def get_all_edges(self):
       return self.G.edges(data=True)
       """
       Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
       :return: gli edges del grafo con gli attributi (il weight)
       """


   def ottieni_citta_per_id(self):
       dizionario = DAO().popola_hub()
       return dizionario