import datetime
import csv

from giocatore import Giocatore

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