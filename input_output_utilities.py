import datetime
import csv

from giocatore import Giocatore

def stampa_menu():
    print('\nMenu:')
    print('| Opzione | Descrizione                          |')
    print('|---------|--------------------------------------|')
    print('| 1       | Visualizza la classifica aggiornata  |')
    print('| 2       | Imposta una sfida                    |')
    print('| 3       | Esito sfide                          |')
    print('| 4       | Segnala Giocatore infortunato        |')
    print('| 5       | Segnala Giocatore Idoneo             |')
    print('| 6       | Cancella giocatore                   |')
    print('| 7       | Aggiungi Giocatore                   |')
    print('| 8       | Visualizza sfide in corso            |')
    print('| 9       | Visualizza stato giocatori           |')
    print('| 10      | Exit programma                       |')


def visualizza_classifica(giocatori):
    if not giocatori:
        print("Nessun giocatore nella classifica al momento.")
        return

    # Calcola la lunghezza massima dei nomi dei giocatori
    max_length = max([len(g.nome + " " + g.cognome) for g in giocatori])

    # Stampa l'intestazione della tabella
    print("Classifica Giocatori:")
    print("| Posizione |", "Nome".ljust(max_length), "|")
    print("|-----------|" + "-" * (max_length + 1) + "|")

    # Stampa i giocatori
    for giocatore in giocatori:
        nome_completo = giocatore.nome + " " + giocatore.cognome
        print(f"| {giocatore.posizione:<9} | {nome_completo.ljust(max_length)} |")

def get_sfidante_and_sfidato():
    sfidante = int(input("Inserisci la posizione del sfidante: "))
    sfidato = int(input("Inserisci la posizione del sfidato: "))
    return sfidante, sfidato
