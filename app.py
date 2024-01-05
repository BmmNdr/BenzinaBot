from time import sleep
from telegramBot import telegramBot
import json
import os

def getBotToken():
    # Specify the file path
    file_path = os.getcwd() + "/Data/json_dati.json"

    # Open the JSON file
    with open(file_path, "r") as file:
        # Read the contents of the file
        json_data = file.read()

        # Parse the JSON data into a dictionary
        data_dict = json.loads(json_data)

    return data_dict["botToken"]

if __name__ == "__main__":
    naftaBot = telegramBot(getBotToken())    
        
    while(True):
        messages = naftaBot.getUpdates()
        
        for msg in messages:
            
            if("text" not in msg["message"]):
                continue
            
            chat_id = msg["message"]["chat"]["id"]
            text = msg["message"]["text"]
            
            print(str(chat_id) + ": " + text)
            
            if(text == "/start"):
                naftaBot.firstLogin(chat_id)
            elif(text == "/carburante"):
                naftaBot.UpdateFuelType(chat_id)
            elif(text == "/capienza"):
                naftaBot.UpdateFuelCap(chat_id)
            elif(text == "/consumo"):
                naftaBot.UpdateFuelCons(chat_id)
            elif(text == "/rifornimento"):
                naftaBot.Refuel(chat_id)
            elif(text.startswith("/")):
                naftaBot.sendMessage(chat_id, "Comando non riconosciuto")
        
        sleep(2)