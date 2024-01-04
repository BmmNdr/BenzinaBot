import requests

BOT_TOKEN = "6383738627:AAEzW1LNl3v3q9PLOxjMChI9F1X2hEkBmsA"

class telegramBot:
    
    def __init__(self):
        self.url = f"https://api.telegram.org/{BOT_TOKEN}"
        self.offset = 0
        
    def getUpdates(self):
        params = {"offset":self.offset} #first update id to visualize
        resp = requests.get(self.url+"/getUpdates", params=params)
        
        data = resp.json()
        if data['ok'] and len(data['result']) != 0: #if there are new messages updates offset
            self.offset=(data['result'][-1]['update_id']) + 1 #-1 --> last element of the list
            
        return data['result']
    
    def sendMessage(self, chat_id, text):
        params = {"chat_id":chat_id, "text":text}
        requests.post(self.url+"/sendMessage", params=params)