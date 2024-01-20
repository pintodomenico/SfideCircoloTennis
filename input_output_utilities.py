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
    
def salva_classifica(giocatori, filename="classifica.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['posizione', 'nome', 'cognome', 'sfidante', 'sfidato', 'infortunato', 'data_infortunio', 'non_sfidabile', 'ultima_sfida_vinta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for giocatore in giocatori:
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

def carica_classifica(filename="classifica.csv"):
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            giocatori = []
            for row in reader:
                giocatore = Giocatore(int(row['posizione']), row['nome'], row['cognome'])
                giocatore.sfidante = row['sfidante'] == 'True'
                giocatore.sfidato = row['sfidato'] == 'True'
                giocatore.infortunato = row['infortunato'] == 'True'
                giocatore.data_infortunio = datetime.datetime.strptime(row['data_infortunio'], '%Y-%m-%d').date() if row['data_infortunio'] else None
                giocatore.non_sfidabile = row['non_sfidabile'] == 'True'
                giocatore.ultima_sfida_vinta = datetime.datetime.strptime(row['ultima_sfida_vinta'], '%Y-%m-%d').date() if row['ultima_sfida_vinta'] else None
                giocatori.append(giocatore)
            return giocatori
    except FileNotFoundError:
        pass

