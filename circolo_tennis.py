import datetime
import csv

from giocatore import Giocatore
from input_output_utilities import *

class CircoloTennis:
    def __init__(self):
        self.giocatori = []
        self.infortunati = []

    def visualizza_classifica(self):
        if not self.giocatori:
            print("Nessun giocatore nella classifica al momento.")
            return

    # Calcola la lunghezza massima dei nomi dei giocatori
        max_length = max([len(g.nome + " " + g.cognome) for g in self.giocatori])

    # Stampa l'intestazione della tabella
        print("Classifica Giocatori:")
        print("| Posizione |", "Nome".ljust(max_length), "|")
        print("|-----------|" + "-" * (max_length + 1) + "|")

    # Stampa i giocatori
        for giocatore in self.giocatori:
            nome_completo = giocatore.nome + " " + giocatore.cognome
            print(f"| {giocatore.posizione:<9} | {nome_completo.ljust(max_length)} |")
    def visualizza_sfide_in_corso(self):
        sfide_attive = [g for g in self.giocatori if g.sfidante or g.sfidato]
        if sfide_attive:
            print("Sfide in corso:")
            for giocatore in sfide_attive:
                if giocatore.sfidante:
                    sfidato = self.giocatori[giocatore.posizione - 2]  # il giocatore successivo nella lista è lo sfidato
                    print(f"{giocatore.nome} {giocatore.cognome} (Sfidante) vs {sfidato.nome} {sfidato.cognome} (Sfidato)")
        else:
            print("Non ci sono sfide in corso al momento.")
    def visualizza_stato_giocatori(self):
        print("Stato dei giocatori:")
        for giocatore in self.giocatori:
            stato = "Sfidabile"
            if giocatore.non_sfidabile:
                stato = "Immune alla sfida"
            elif giocatore.sfidato:
                stato = "Sfidato"
            elif giocatore.infortunato:
                stato = "Infortunato"
            elif giocatore.sfidante:
                stato = "Sfidante"
            print(f"{giocatore.nome} {giocatore.cognome} - {stato}")

    def imposta_sfida(self, sfidante_posizione, sfidato_posizione):
        sfidante = self.giocatori[sfidante_posizione - 1]
        sfidato = self.giocatori[sfidato_posizione - 1]

        if sfidante.infortunato or sfidato.infortunato:
            print("Non puoi impostare una sfida con giocatori infortunati.")
            return

        if sfidante.sfidante or sfidato.sfidante or sfidante.sfidato or sfidato.sfidato:
            print("Uno dei giocatori è già coinvolto in un'altra sfida.")
            return

        if sfidante.posizione < sfidato.posizione or (sfidante.posizione - sfidato.posizione) != 1:
            print("Sfida non ammessa.")
            return
        if not sfidante.puo_sfidare:
            print(f"{sfidante.nome} {sfidante.cognome} ha perso l'ultima sfida e non può sfidare al momento.")
            return

        if sfidato.puo_sfidare:
            print(f"{sfidato.nome} {sfidato.cognome} ha vinto l'ultima sfida e non può essere sfidato al momento.")
            return

        sfidante.sfidante = True
        sfidato.sfidato = True
        print(f"Sfida impostata tra {sfidante.nome} {sfidante.cognome} e {sfidato.nome} {sfidato.cognome}.")

    def esito_sfida(self):
    # Trova la sfida attiva
        for giocatore in self.giocatori:
            if giocatore.sfidante:
                sfidante = giocatore
                sfidato = self.giocatori[giocatore.posizione - 2]
                break
        else:
            print("Non ci sono sfide attive al momento.")
            return

    # Chiedi chi ha vinto
        print(f"Sfida tra {sfidante.nome} {sfidante.cognome} (Sfidante) e {sfidato.nome} {sfidato.cognome} (Sfidato)")
        vincitore = input("Chi ha vinto? (Inserisci 'Sfidante' o 'Sfidato'): ")

    # Aggiorna le posizioni in base al vincitore
        if vincitore == "Sfidante":
            self.giocatori[sfidante.posizione - 1], self.giocatori[sfidato.posizione - 1] = sfidato, sfidante
            sfidante.posizione, sfidato.posizione = sfidato.posizione, sfidante.posizione
            sfidante.puo_sfidare = True
            sfidato.puo_sfidare = False
            print(f"{sfidante.nome} {sfidante.cognome} vince la sfida e scambia posizione con {sfidato.nome} {sfidato.cognome}.")
        elif vincitore == "Sfidato":
            sfidato.puo_sfidare = True
            sfidante.puo_sfidare = False
            print(f"{sfidato.nome} {sfidato.cognome} vince la sfida e mantiene la sua posizione.")
        else:
            print("Selezione non valida. Riprova.")

    # Resetta lo stato della sfida per entrambi i giocatori
        sfidante.sfidante = False
        sfidato.sfidato = False

    def segnala_infortunato(self, giocatore_posizione):
        giocatore = self.giocatori[giocatore_posizione - 1]

        if giocatore.infortunato:
            print("Questo giocatore è già infortunato.")
            return

        giocatore.infortunato = True
        giocatore.data_infortunio = datetime.date.today()
        print(f"{giocatore.nome} {giocatore.cognome} è stato segnalato come infortunato.")

        # Scala automaticamente di una posizione
        if giocatore_posizione < len(self.giocatori):
            giocatore_successivo = self.giocatori[giocatore_posizione]
            self.giocatori[giocatore_posizione - 1], self.giocatori[giocatore_posizione] = giocatore_successivo, giocatore
            giocatore.posizione, giocatore_successivo.posizione = giocatore_successivo.posizione, giocatore.posizione

    def segnala_idoneo(self, giocatore_posizione):
        giocatore = self.giocatori[giocatore_posizione - 1]

        if not giocatore.infortunato:
            print("Questo giocatore non è infortunato.")
            return

        ore_trascorse = (datetime.datetime.now() - datetime.datetime.combine(giocatore.data_infortunio, datetime.time())).total_seconds() / 3600
        if ore_trascorse < 24:
            print(f"{giocatore.nome} {giocatore.cognome} non può ancora rientrare. Sono trascorse solo {int(ore_trascorse)} ore dall'infortunio.")
            return

        giocatore.infortunato = False
        giocatore.data_infortunio = None
        print(f"{giocatore.nome} {giocatore.cognome} è nuovamente idoneo.")

    def cancella_giocatore(self, giocatore_posizione):
        if 0 < giocatore_posizione <= len(self.giocatori):
            giocatore_rimosso = self.giocatori.pop(giocatore_posizione - 1)
            print(f'{giocatore_rimosso.nome} {giocatore_rimosso.cognome} è stato rimosso dalla classifica.')
            # Aggiornamento delle posizioni dei giocatori rimanenti
            for idx, giocatore in enumerate(self.giocatori[giocatore_posizione-1:], start=giocatore_posizione):
                giocatore.posizione = idx
        else:
            print('Posizione non valida.')

    def aggiungi_giocatore(self, nome, cognome):
        if len(self.giocatori) < 56:
            posizione = len(self.giocatori) + 1
            nuovo_giocatore = Giocatore(posizione, nome, cognome)
            self.giocatori.append(nuovo_giocatore)
            print(f'{nome} {cognome} è stato aggiunto alla posizione {posizione}.')
        else:
            print('La classifica ha raggiunto il limite massimo di giocatori.')

    def aggiorna_infortunati(self):
        for giocatore in self.giocatori:
            if giocatore.infortunato and (datetime.date.today() - giocatore.data_infortunio).days % 30 == 0:
                posizione_attuale = giocatore.posizione
                if posizione_attuale < len(self.giocatori):
                    giocatore_successivo = self.giocatori[posizione_attuale]
                    self.giocatori[posizione_attuale - 1], self.giocatori[posizione_attuale] = giocatore_successivo, giocatore
                    giocatore.posizione, giocatore_successivo.posizione = giocatore_successivo.posizione, giocatore.posizione
                    print(f"{giocatore.nome} {giocatore.cognome} è sceso di una posizione a causa dell'infortunio.")
    def aggiorna_posizione_infortunati(self):
        for giocatore in self.giocatori:
            if giocatore.infortunato:
                giorni_trascorsi = (datetime.date.today() - giocatore.data_infortunio).days
                if giorni_trascorsi == 30 or (giorni_trascorsi > 30 and (giorni_trascorsi - 30) % 15 == 0):
                    posizione_attuale = giocatore.posizione
                    if posizione_attuale < len(self.giocatori):
                        giocatore_successivo = self.giocatori[posizione_attuale]
                        self.giocatori[posizione_attuale - 1], self.giocatori[posizione_attuale] = giocatore_successivo, giocatore
                        giocatore.posizione, giocatore_successivo.posizione = giocatore_successivo.posizione, giocatore.posizione
                        print(f"{giocatore.nome} {giocatore.cognome} è sceso di una posizione a causa dell'infortunio.")          

    def aggiorna_non_sfidabili(self):
        for giocatore in self.giocatori:
            if giocatore.non_sfidabile and (datetime.date.today() - giocatore.ultima_sfida_vinta).days >= 30:
                giocatore.non_sfidabile = False
                print(f"{giocatore.nome} {giocatore.cognome} può ora essere sfidato di nuovo.")

    def verifica_sfide(self):
        for giocatore in self.giocatori:
            if giocatore.sfidante and giocatore.ultima_sfida_vinta and (datetime.date.today() - giocatore.ultima_sfida_vinta).days >= 7:
                giocatore.non_sfidabile = True
                print(f"{giocatore.nome} {giocatore.cognome} non può essere sfidato per 30 giorni.")

    def salva_classifica(self, filename="classifica.csv"):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['posizione', 'nome', 'cognome', 'sfidante', 'sfidato', 'infortunato', 'data_infortunio', 'non_sfidabile', 'ultima_sfida_vinta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for giocatore in self.giocatori:
                writer.writerow({
                    'posizione': giocatore.posizione,
                    'nome': giocatore.nome,
                    'cognome': giocatore.cognome,
                    'sfidante': giocatore.sfidante,
                    'sfidato': giocatore.sfidato,
                    'infortunato': giocatore.infortunato,
                    'data_infortunio': giocatore.data_infortunio.strftime('%Y-%m-%d') if giocatore.data_infortunio else '',
                    'non_sfidabile': giocatore.non_sfidabile,
                    'ultima_sfida_vinta': giocatore.ultima_sfida_vinta.strftime('%Y-%m-%d') if giocatore.ultima_sfida_vinta else ''
                })

    def carica_classifica(self, filename="classifica.csv"):
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                self.giocatori = []
                for row in reader:
                    giocatore = Giocatore(int(row['posizione']), row['nome'], row['cognome'])
                    giocatore.sfidante = row['sfidante'] == 'True'
                    giocatore.sfidato = row['sfidato'] == 'True'
                    giocatore.infortunato = row['infortunato'] == 'True'
                    giocatore.data_infortunio = datetime.datetime.strptime(row['data_infortunio'], '%Y-%m-%d').date() if row['data_infortunio'] else None
                    giocatore.non_sfidabile = row['non_sfidabile'] == 'True'
                    giocatore.ultima_sfida_vinta = datetime.datetime.strptime(row['ultima_sfida_vinta'], '%Y-%m-%d').date() if row['ultima_sfida_vinta'] else None
                    self.giocatori.append(giocatore)
        except FileNotFoundError:
            pass