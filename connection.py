import mysql.connector

#Utenti(ID, tipoCarburante, Consumo, Capienza)
#Prezzi(idImpianto*, tipoCarburante, prezzo, isSelf, dtComu)
#Impianti(idImpianto, Gestore, Bandiera, TipoImpianto, NomeImpianto, Indirizzo, Comune, Provincia, Latitudine, Longitudine)

class connection:
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_botbenzina"
            )
        
    