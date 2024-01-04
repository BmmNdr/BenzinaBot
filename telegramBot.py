import requests
import time

BOT_TOKEN = "bot6450047602:AAHYA1jfTMs0DQ94YUi1NFex52v3tRMMLbo"

class telegramBot:
    
    def __init__(self):
        self.url = f"https://api.telegram.org/{BOT_TOKEN}"
        self.offset = 0
    
    #get new messages received by the bot
    def getUpdates(self):
        params = {"offset":self.offset} #first update id to visualize
        resp = requests.get(self.url+"/getUpdates", params=params)
        
        data = resp.json()
        if data['ok'] and len(data['result']) != 0: #if there are new messages updates offset
            self.offset=(data['result'][-1]['update_id']) + 1 #-1 --> last element of the list
            
        return data['result']
    
    #gets a message from a specific chat (for 30s)
    def getReply(self, chat_id): 
        lastUpdateID = self.offset #internal offset to get only new messages
        
        start_time = time.time()

        while time.time() - start_time < 30:
            params = {"offset":lastUpdateID}
            resp = requests.get(self.url+"/getUpdates", params=params)
            
            data = resp.json()
            
            for e in data["result"]:
                lastUpdateID = e["update_id"] + 1
                
                if(e["message"]["chat"]["id"] == chat_id):
                    return e["message"]["text"]
                
        return None
    
    #send a message to a specific chat
    def sendMessage(self, chat_id, text):
        params = {"chat_id":chat_id, "text":text}
        requests.post(self.url+"/sendMessage", params=params)
        
    #update the type of fuel
    def UpdateFuelType(self, chat_id):
        self.sendMessage(chat_id, "Inserire il nuovo tipo di carburante")
        
        reply = self.getReply(chat_id)
        
        if(reply != None):
            print(reply) #TODO: save in db
        else:
            self.sendMessage(chat_id, "Hai impiegato troppo tempo per inserire il tipo di carburante. Riprova il comando")
            
    #update the capacity of the tank
    def UpdateFuelCap(self, chat_id):
        self.sendMessage(chat_id, "Inserire la nuova capienza del serbatoio")
        
        reply = self.getReply(chat_id)
        
        if(reply != None):
            print(reply) #TODO: save in db
        else:
            self.sendMessage(chat_id, "Hai impiegato troppo tempo per inserire la nuova capienza. Riprova il comando")
        
    #make a refueling
    def Refuel(self, chat_id): #TODO
        params = {"chat_id":chat_id, "text":text}
        requests.post(self.url+"/sendMessage", params=params)