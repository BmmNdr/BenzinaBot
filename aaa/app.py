import requests
from time import sleep
import time
BOT_TOKEN = "bot6691376374:AAFtA-CdROHY7ycSGusyxFy2HZGPtNjrrKY"
url = f"https://api.telegram.org/{BOT_TOKEN}/getUpdates"

offset = 0
start_time = time.time()

while time.time() - start_time < 60:
    parametri = {"offset":offset} #primo update id che voglio visualizzare

    resp = requests.get(url, params=parametri)
    data = resp.json()

    #elaborazione dei dati
    #print(data)

    for e in data["result"]:
        lastUpdateID=e["update_id"]
        
        #print(e["message"]["chat"]["id"])
        
    print(lastUpdateID)

    #cambio l'offset
    #if(len(data["result"]) > 0):
    #    offset += lastUpdateID + 1

    sleep(5)   
    
    
print("A minute has passed")