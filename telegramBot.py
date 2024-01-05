import json
import requests
from connection import connection
from datetime import datetime
import os

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

class telegramBot:
    def __init__(self, bot_token):
        self.url = f"https://api.telegram.org/{bot_token}"
        self.offset = 0
        self.conn = connection()
        
        if(shouldUpdateDB()):
            print("Aggiornamento dati...")
            self.conn.uploadData()
            print("Dati aggiornati")
        else:
            print("Dati già aggiornati")  
    
    #get new messages received by the bot
    def getUpdates(self):
        params = {"offset":self.offset} #first update id to visualize
        resp = requests.get(self.url+"/getUpdates", params=params)
        
        data = resp.json()
        if data['ok'] and len(data['result']) != 0: #if there are new messages updates offset
            self.offset=(data['result'][-1]['update_id']) + 1 #-1 --> last element of the list
            
        return data['result']
    
    #gets a message from a specific chat (for 30s)
    def getReply(self, chat_id, offset): 
        lastUpdateID = max(self.offset, offset) #internal offset to get only new messages
        
        #start_time = time.time()

        #while time.time() - start_time < 30:
        while True:
            params = {"offset":lastUpdateID}
            resp = requests.get(self.url+"/getUpdates", params=params)
            
            data = resp.json()
            
            for e in data["result"]:                
                if(e["message"]["chat"]["id"] == chat_id):
                    return e["message"]["text"], lastUpdateID
                
                lastUpdateID = e["update_id"] + 1
    
    #send a message to a specific chat
    def sendMessage(self, chat_id, text, keyboard=None):
        params = {"chat_id":chat_id, "text":text, "reply_markup":keyboard}
        requests.post(self.url+"/sendMessage", params=params)
        
    def getKeyboard(self):
        return [[{"text":"Benzina"}], [{"text":"Diesel"}], [{"text":"GPL"}], [{"text":"Metano"}]]
        
    #update the type of fuel
    def UpdateFuelType(self, chat_id, offset=0, firstTime=False):
        self.sendMessage(chat_id, "Inserire il tipo di carburante", keyboard=json.dumps({"keyboard":self.getKeyboard(), "is_persistent":True, "one_time_keyboard":True}))
        
        reply, offset = self.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "tipoCarburante", reply)
            
    #update the capacity of the tank
    def UpdateFuelCap(self, chat_id, offset=0, firstTime=False):
        self.sendMessage(chat_id, "Inserire la capienza del serbatoio")
        
        reply, offset = self.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "Capienza", reply)
        
    #update the average fuel consumption
    def UpdateFuelCons(self, chat_id, offset=0, firstTime=False):
        self.sendMessage(chat_id, "Inserire il consumo medio (l/100km)")
        
        reply, offset = self.getReply(chat_id, offset)
        
        if(firstTime):
            return reply, offset
        
        self.conn.updateUser(chat_id, "Consumo", reply)
        
    def firstLogin(self, chat_id):
        
        
        if(self.conn.getUser(chat_id) == []):
            self.sendMessage(chat_id, "Benvenuto nel Nafta bot")
            fuelType, offset = self.UpdateFuelType(chat_id, self.offset, True)
            fuelCap, offset = self.UpdateFuelCap(chat_id, offset + 1, True)
            fuelCons, offset = self.UpdateFuelCons(chat_id, offset + 1, True)
            self.conn.insertUser(chat_id, fuelType, fuelCons, fuelCap)
        else:
            self.sendMessage(chat_id, "Bentornato nel Nafta bot")
        
    #make a refueling
    def Refuel(self, chat_id): #TODO
        self.sendMessage(chat_id, "Rifornimento")