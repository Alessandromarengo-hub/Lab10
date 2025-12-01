import flet as ft
from UI.view import View
from model.model import Model




class Controller:
   def __init__(self, view: View, model: Model):
       self._view = view
       self._model = model


   def mostra_tratte(self, e):
       """
       Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
       popola "self._view.lista_visualizzazione" con le seguenti info
       * Numero di Hub presenti
       * Numero di Tratte
       * Lista di Tratte che superano il costo indicato come soglia
       """
       soglia = float(self._view.guadagno_medio_minimo.value)
       self._view.lista_visualizzazione.controls.clear()
       self._model.pulizia()
       self._model.costruisci_grafo(soglia)
       associa_id_citta = self._model.ottieni_citta_per_id()


       numero_nodi = self._model.get_num_nodes()
       numero_tratte = self._model.get_num_edges()
       self._view.lista_visualizzazione.controls.append(
           ft.Text(f"📌 Numero di Hub (nodi): {numero_nodi}")
       )
       self._view.lista_visualizzazione.controls.append(
           ft.Text(f"📌 Numero di Tratte (edges): {numero_tratte}")
       )
       self._view.lista_visualizzazione.controls.append(
           ft.Text("📎 Lista delle tratte che superano la soglia:")
       )


       # 5️⃣ Stampa edges con peso
       for u, v, data in self._model.G.edges(data=True):
           valore = data["weight"]
           self._view.lista_visualizzazione.controls.append(
               ft.Text(f" - {associa_id_citta[u].citta} ({associa_id_citta[u].stato}) "
                       f"↔ {associa_id_citta[v].citta}, ({associa_id_citta[v].stato})"
                       f" guadagno medio: {valore:.2f}")
           )


       self._view.update()
