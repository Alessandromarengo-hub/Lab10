from database.DB_connect import DBConnect
from model.grafo import Grafo
from model.hub import Hub

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def grafo_filtrato(threshold):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f"""SELECT 
                        LEAST(id_hub_origine, id_hub_destinazione) AS hub1,
                        GREATEST(id_hub_origine, id_hub_destinazione) AS hub2,
                        AVG(valore_merce) AS media_valore
                    FROM spedizione
                    GROUP BY 
                        LEAST(id_hub_origine, id_hub_destinazione),
                        GREATEST(id_hub_origine, id_hub_destinazione)
                    HAVING AVG(valore_merce) > {threshold};
                    """
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                graph = Grafo(
                    id_hub_arrivo=row["hub1"],
                    id_hub_partenza=row["hub2"],
                    valore_tratta=row["media_valore"],
                )

                result.append(graph)
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    def popola_hub(self):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f""" SELECT id, codice, nome, citta, stato, longitudine, latitudine
                    FROM hub"""
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                h = Hub(
                    id=row["id"],
                    nome=row["nome"],
                    codice = row["codice"],
                    citta =row["citta"],
                    stato = row["stato"],
                    longitudine= row["longitudine"],
                    latitudine = row["latitudine"]
                )
                result[h.id] = h

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    # TODO
