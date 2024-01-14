import requests

class telegramBot:
    def __init__(self, bot_token):
        self.url = f"https://api.telegram.org/{bot_token}"
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
    def getReply(self, chat_id, offset, position=False): 
        lastUpdateID = max(self.offset, offset) #internal offset to get only new messages
        
        #start_time = time.time()

        #while time.time() - start_time < 30:
        while True:
            params = {"offset":lastUpdateID}
            resp = requests.get(self.url+"/getUpdates", params=params)
            
            data = resp.json()
            
            for e in data["result"]:             
                lastUpdateID = e["update_id"] + 1
                   
                if(e["message"]["chat"]["id"] == chat_id and position == False):
                    return e["message"]["text"], lastUpdateID
                elif(e["message"]["chat"]["id"] == chat_id and position == True):
                    return e["message"]["location"], lastUpdateID
                    
    #send a message to a specific chat
    def sendMessage(self, chat_id, text, keyboard=None):
        params = {"chat_id":chat_id, "text":text, "reply_markup":keyboard}
        requests.post(self.url+"/sendMessage", params=params)
        
    def sendLocation(self, chat_id, latitude, longitude):
        params = {"chat_id":chat_id, "latitude":latitude, "longitude":longitude}
        requests.post(self.url+"/sendLocation", params=params)