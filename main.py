from circolo_tennis import CircoloTennis
from input_output_utilities import stampa_menu

def main():
    print("Versione del programma: 1.22 funzionanate")
    circolo = CircoloTennis()
    circolo.carica_classifica()

    while True:
        circolo.aggiorna_posizione_infortunati() 
        stampa_menu()

        try:
            scelta = input('Inserisci il numero dell\'azione desiderata: ')

            if scelta == '1':
                circolo.visualizza_classifica()
            elif scelta == '2':
                sfidante = int(input("Inserisci la posizione del sfidante: "))
                sfidato = int(input("Inserisci la posizione del sfidato: "))
                circolo.imposta_sfida(sfidante, sfidato)
            elif scelta == '3':
                circolo.esito_sfida()
            elif scelta == '4':
                infortunato = int(input("Inserisci la posizione del giocatore infortunato: "))
                circolo.segnala_infortunato(infortunato)
            elif scelta == '5':
                idoneo = int(input("Inserisci la posizione del giocatore idoneo: "))
                circolo.segnala_idoneo(idoneo)
            elif scelta == '6':
                da_cancellare = int(input("Inserisci la posizione del giocatore da cancellare: "))
                circolo.cancella_giocatore(da_cancellare)
            elif scelta == '7':
                nome = input("Inserisci il nome del nuovo giocatore: ")
                cognome = input("Inserisci il cognome del nuovo giocatore: ")
                circolo.aggiungi_giocatore(nome, cognome)
            elif scelta == '8':
                circolo.visualizza_sfide_in_corso()
            elif scelta == '9':
                circolo.visualizza_stato_giocatori()
            elif scelta == '10':
                circolo.salva_classifica()
                break
            else:
                print("Scelta non valida. Riprova.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

if __name__ == '__main__':
    main()