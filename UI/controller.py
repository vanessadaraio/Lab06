import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    # TODO

    def mostra_strumento(self,e):
        strumenti=self._model.get_strumenti() # il controller chiama il metodo get_strumenti() del Model

        self._view.lista_strumenti.controls.clear() # elimina tutti gli elementi presenti nella listview( serve per evitare che, premendo
                                                    # più volte Mostra gli stessi strumenti vengano aggiunti ripetutamente

        if strumenti is None:
            self._view.show_alert('Errore nel recupero degli strumenti')
            return

        if len(strumenti)==0:
            self._view.show_alert('non ci strumenti nel deposito')
            return

        for strumento in strumenti:
            self._view.lista_strumenti.controls.append(ft.Text(str(strumento))) #str(strumento) richiama il metodo __str__() della classe Strumento

        self._view.update()

    def cerca_tipo_strumento(self,e):
        tipo=self._view.input_tipo_strumento.value

        if tipo is None or tipo.strip()=='':
            self._view.show_alert('inserisci il tipo di strumento da cercare!')
            return

        strumenti=self._model.cerca_strumenti_per_tipo(tipo.strip())
        self._view.lista_strumenti_ricerca.controls.clear()

        if strumenti is None:
            self._view.show_alert('errore durante la ricerca')
            return

        if len(strumenti)==0:
            self._view.show_alert('nessuno strumento trovato')
            return

        for strumento in strumenti:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento))) #inseriamo nella listView tutti gli strumenti trovati 
        self._view.update()
