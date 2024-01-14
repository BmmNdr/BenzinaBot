import json
from connection import connection
from openroute import openroute
from datetime import datetime
from telegramBot import telegramBot
import os
import re

def shouldUpdateDB():
        # Specify the file path
        file_path = os.getcwd() + "/Data/json_dati.json"

        # Open the JSON file
        with open(file_path, "r") as file:
            # Read the contents of the file
            json_data = file.read()

            # Parse the JSON data into a dictionary
            data_dict = json.loads(json_data)

        if(data_dict["date"] != datetime.today().strftime('%Y-%m-%d')):
            data_dict["date"] = datetime.today().strftime('%Y-%m-%d') 

            with open(file_path, "w") as outfile:
                json.dump(data_dict, outfile)
        
            return True
        
        return False

class service:
    def __init__(self, bot_token, openRouteToken):
        self.conn = connection()
        self.openRoute = openroute(openRouteToken)
        self.telegramBot = telegramBot(bot_token)
        
        if(shouldUpdateDB()):
            print("Aggiornamento dati...")
            self.conn.uploadData()
            print("Dati aggiornati")
        else:
            print("Dati già aggiornati")  
        
    def getKeyboard(self):
        return [[{"text":"Benzina"}], [{"text":"Diesel"}], [{"text":"GPL"}], [{"text":"Metano"}]]
        
    #update the type of fuel
    def UpdateFuelType(self, chat_id, offset=0, firstTime=False):
        telegramBot.sendMessage(chat_id, "Inserire il tipo di carburante", keyboard=json.dumps({"keyboard":self.getKeyboard(), "is_persistent":True, "one_time_keyboard":True}))
        
        offset = max(telegramBot.offset, offset)
        
        reply, offset = telegramBot.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "tipoCarburante", reply)
        telegramBot.sendMessage(chat_id, "Carburante aggiornato")
            
    #update the capacity of the tank
    def UpdateFuelCap(self, chat_id, offset=0, firstTime=False):
        offset = max(telegramBot.offset, offset)
        
        reply = 'a'
        
        while(re.match(r'^(([0-9]+)(\.([0-9]+))?)$', reply) is None):
            telegramBot.sendMessage(chat_id, "Inserire la capienza del serbatoio")
            reply, offset = telegramBot.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "Capienza", reply)
        telegramBot.sendMessage(chat_id, "Capienza aggiornata")
        
    #update the average fuel consumption
    def UpdateFuelCons(self, chat_id, offset=0, firstTime=False):
        offset = max(telegramBot.offset, offset)
        
        reply = 'a'
        
        while(re.match(r'^(([0-9]+)(\.([0-9]+))?)$', reply) is None):
            telegramBot.sendMessage(chat_id, "Inserire il consumo medio (l/100km)")
            reply, offset = telegramBot.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "Consumo", reply)
        
    def firstLogin(self, chat_id):
        if(self.conn.getUser(chat_id) == []):
            telegramBot.sendMessage(chat_id, "Benvenuto nel Nafta bot")
            fuelType, offset = self.UpdateFuelType(chat_id, self.offset, True)
            fuelCap, offset = self.UpdateFuelCap(chat_id, offset, True)
            fuelCons, offset = self.UpdateFuelCons(chat_id, offset, True)
            self.conn.insertUser(chat_id, fuelType, fuelCons, fuelCap)
            telegramBot.sendMessage(chat_id, "Registrazione effettuata")
        else:
            telegramBot.sendMessage(chat_id, "Bentornato nel Nafta bot")
        
    #make a refueling
    def Refuel(self, chat_id):
        telegramBot.sendMessage(chat_id, "Quanto vuoi rifornire?", keyboard=json.dumps({"keyboard":[[{"text":"1/4"}], [{"text":"Meta'"}], [{"text":"Pieno"}]], "is_persistent":True, "one_time_keyboard":True}))
        quantity, offset = telegramBot.getReply(chat_id, telegramBot.offset)
        
        if(quantity == "1/4"):
            quantity = 0.25
        elif(quantity == "Meta'"):
            quantity = 0.5
        else:
            quantity = 1
        
        telegramBot.sendMessage(chat_id, "Dove ti trovi al momento?", keyboard=json.dumps({"keyboard":[[{"text":"Posizione", "request_location":True}]], "is_persistent":True, "one_time_keyboard":True}))
        location, offset = telegramBot.getReply(chat_id, offset, position=True)
        
        stations = self.conn.getUserStations(chat_id)
        
        telegramBot.sendMessage(chat_id, "Sto calcolando il miglior benzinaio...")
        
        minID, minPrice = self.openRoute.findBest(location, stations, quantity * self.conn.getFromUser(chat_id, "Capienza")[0][0], self.conn.getFromUser(chat_id, "Consumo")[0][0])
        
        station = self.conn.getStation(minID)
        
        telegramBot.sendMessage(chat_id, f"Il Benzinaio piu' conveniente e' {station[0]['NomeImpianto']} a ({station[0]['Comune']}), il prezzo totale e' {minPrice} euro")
        
        telegramBot.sendLocation(chat_id, station[0]["Latitudine"], station[0]["Longitudine"])