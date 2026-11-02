from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        # TODO
        cnx=get_connection() # connessione al database,get_connection() richiama la funzione presente in DB_connect
        if cnx is None:
            return None

        try:
            cursor = cnx.cursor() # creazione del cursore
            query='SELECT * FROM strumento'
            cursor.execute(query)

            risultati=cursor.fetchall() #fetchall() recupera tutte le righe restituite dalla query

            lista_strumenti=[] # creiamo lista vuota nel quale inseriremo tutti gli oggetti Strumento

            for riga in  risultati:
                #trasformiamo ogni riga del database in un oggetto della classe Strumento
                strumento=Strumento(riga[0],
                                    riga[1],
                                    riga[2],
                                    riga[3],
                                    riga[4],
                                    riga[5])
                lista_strumenti.append(strumento)
            return lista_strumenti

        except Exception as e:
            print(f'errore durante il recupero degli strumenti:{e}')
            return None

        finally: # il blocco finally viene eseguito anche se si verifica un errore. Cosi evitiamo di lasciare connessioni aperte
            if 'cursor' in locals():
                cursor.close() # chiude il cursore
            cnx.close()        #chiude la connessione al database



    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        # TODO
        if tipo is None or tipo.strip()=='':
            return []
        cnx=get_connection()

        if cnx is None:
            return None

        cursor=None

        try:
            cursor = cnx.cursor()
            query='SELECT * FROM strumento WHERE tipo = %s'
            cursor.execute(query, (tipo.strip(),)) # virgola dopo tipo necessaria pk python deve interpretare (tipo,) come una tupla con un solo elemento

            risultati=cursor.fetchall() # recuperiamo tutte le righe che soddisfano la condizione

            lista_strumenti=[]
            for riga in risultati:
                strumento=Strumento(riga[0],
                                    riga[1],
                                    riga[2],
                                    riga[3],
                                    riga[4],
                                    riga[5])
                lista_strumenti.append(strumento)

            return lista_strumenti
        except Exception as e:
            print(f'errore durante la ricerca degli strumenti:{e}')
            return None

        finally:
            if cursor is not None:
                cursor.close()
            cnx.close()

