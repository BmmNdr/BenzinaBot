import mysql.connector
import requests

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
        
    def readCSV(self, url):
        req = requests.get(url)
        url_content = req.content
        
        url_content = url_content.split(sep=b"\n")
        data = url_content[2:]
        
        return data
        
    def uploadPrezzi(self):
        data = self.readCSV("https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv")
        
        print("Aggiornamento prezzi...")
        
        for prezzo in data:
            prezzo = prezzo.decode("utf-8")
            prezzo = prezzo.split(sep=";")
            
            if(len(prezzo) >= 3):
                idImpianto = prezzo[0]
                tipoCarburante = prezzo[1]
                valPrezzo = prezzo[2]
                isSelf = prezzo[3]
                
                if((tipoCarburante == "Benzina" or tipoCarburante == "Diesel" or tipoCarburante == "GPL" or tipoCarburante == "Metano") and isSelf == "0"):
                    try:
                        mycursor = self.mydb.cursor()
                        mycursor.execute("INSERT INTO Prezzi (idImpianto, tipoCarburante, prezzo) VALUES (%s, %s, %s)", (idImpianto, tipoCarburante, valPrezzo))
                        self.mydb.commit()
                        mycursor.close()
                    except mysql.connector.Error as err:
                        #print("Error inserting data into Prezzi table:", err)
                        try:
                            mycursor = self.mydb.cursor()
                            mycursor.execute("UPDATE Prezzi SET prezzo = %s WHERE idImpianto = %s AND tipoCarburante = %s", (valPrezzo, idImpianto, tipoCarburante))
                            self.mydb.commit()
                            mycursor.close()
                            #print("Data updated in Prezzi table")
                        except mysql.connector.Error as err:
                            print("Error updating data in Prezzi table:", err)
                
        print("Prezzi aggiornati")
            
    def uploadStations(self):
        
        print("Aggiornamento impianti...")
        
        data = self.readCSV("https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv")  
        
        for impianto in data:
            impianto = impianto.decode("utf-8")
            impianto = impianto.split(sep=";")
            
            if(len(impianto) == 10):
                idImpianto = impianto[0]
                Gestore = impianto[1]
                Bandiera = impianto[2]
                TipoImpianto = impianto[3]
                NomeImpianto = impianto[4]
                Indirizzo = impianto[5]
                Comune = impianto[6]
                Provincia = impianto[7]
                Latitudine = impianto[8]
                Longitudine = impianto[9]
                
                try:
                    mycursor = self.mydb.cursor()
                    mycursor.execute("INSERT INTO Impianti (idImpianto, Gestore, Bandiera, TipoImpianto, NomeImpianto, Indirizzo, Comune, Provincia, Latitudine, Longitudine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (idImpianto, Gestore, Bandiera, TipoImpianto, NomeImpianto, Indirizzo, Comune, Provincia, Latitudine, Longitudine))
                    self.mydb.commit()
                    mycursor.close()
                except mysql.connector.Error as err:
                    try:
                        mycursor = self.mydb.cursor()
                        mycursor.execute("UPDATE Impianti SET Gestore = %s, Bandiera = %s, TipoImpianto = %s, NomeImpianto = %s, Indirizzo = %s, Comune = %s, Provincia = %s, Latitudine = %s, Longitudine = %s WHERE idImpianto = %s", (Gestore, Bandiera, TipoImpianto, NomeImpianto, Indirizzo, Comune, Provincia, Latitudine, Longitudine, idImpianto))
                        self.mydb.commit()
                        mycursor.close()
                        #print("Data updated in Impianti table")
                    except mysql.connector.Error as err:
                        print("Error updating data in Impianti table:", err)
                
        print("Impianti aggiornati")
        
    def uploadData(self):
        self.uploadStations()
        self.uploadPrezzi()
    
    def insertUser(self, chat_id, fuelType, fuelCons, fuelCap):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("INSERT INTO users (ID, tipoCarburante, Consumo, Capienza) VALUES (%s, %s, %s, %s)", (chat_id, fuelType, fuelCons, fuelCap))
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            print("Error inserting data into users table:", err)    
            
    def updateUser(self, chatId, colName, value):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(f"UPDATE users SET {colName}" + " = %s WHERE ID = %s", (value, chatId))
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            print("Error updating data in users table:", err)
            
    def getUser(self, chatId):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(f"SELECT * FROM users WHERE ID = {chatId}")
            myresult = mycursor.fetchall()
            mycursor.close()
            
            return myresult
        except mysql.connector.Error as err:
            print("Error getting data from users table:", err)
            
    def getFromUser(self, chatId, colName):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(f"SELECT {colName} FROM users WHERE ID = {chatId}")
            myresult = mycursor.fetchall()
            mycursor.close()
            
            return myresult
        except mysql.connector.Error as err:
            print("Error getting data from users table:", err)
            
    def getUserStations(self, chatId):
        try:
            
            fuelType = self.getFromUser(chatId, "tipoCarburante")[0][0]
            
            mycursor = self.mydb.cursor()
            mycursor.execute(f"SELECT * FROM Impianti JOIN Prezzi ON Impianti.idImpianto = Prezzi.IdImpianto WHERE tipoCarburante = '{fuelType}'")
            
            #return a DB as dictionary
            myresult = [dict((mycursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in mycursor.fetchall()]
            
            #myresult = mycursor.fetchall()
            
            mycursor.close()
            return myresult
        except mysql.connector.Error as err:
            print("Error getting data from Impianti table:", err)
            
    def getStation(self, idImpianto):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(f"SELECT * FROM Impianti WHERE idImpianto = {idImpianto}")
            
            #return a DB as dictionary
            myresult = [dict((mycursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in mycursor.fetchall()]
            
            #myresult = mycursor.fetchall()
            mycursor.close()
            
            return myresult
        except mysql.connector.Error as err:
            print("Error getting data from Impianti table:", err)