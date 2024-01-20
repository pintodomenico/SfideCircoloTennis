class Giocatore:
    def __init__(self, posizione, nome, cognome):
        self.posizione = posizione
        self.nome = nome
        self.cognome = cognome
        self.sfidante = None
        self.sfidato = None
        self.infortunato = False
        self.data_infortunio = None
        self.non_sfidabile = False
        self.ultima_sfida_vinta = None
        self.puo_sfidare = True

    def __str__(self):
        return f"{self.posizione} {self.nome} {self.cognome}"