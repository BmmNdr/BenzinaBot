import requests
from time import sleep
from telegramBot import telegramBot
from connection import connection
import os
import json
from datetime import datetime

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

def shouldUpdate():
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
    

if __name__ == "__main__":
    naftaBot = telegramBot(getBotToken())
    conn = connection()
    
    if(shouldUpdate()):
        print("Aggiornamento dati...")
        conn.uploadData()
        print("Dati aggiornati")
    else:
        print("Dati già aggiornati")  
        
    while(True):
        messages = naftaBot.getUpdates()
        
        for msg in messages:
            chat_id = msg["message"]["chat"]["id"]
            text = msg["message"]["text"]
            
            print(str(chat_id) + ": " + text)
            
            if(text == "/start"):
                naftaBot.sendMessage(chat_id, "Benvenuto nel Nafta bot")
            elif(text == "/aggiornacarburante"):
                naftaBot.UpdateFuelType(chat_id)
            elif(text == "/aggiornacapienza"):
                naftaBot.UpdateFuelCap(chat_id)
            elif(text == "/rifornimento"):
                naftaBot.Refuel(chat_id)
            
            #else: #crea problema con getReply
            #    naftaBot.sendMessage(chat_id, "Comando non riconosciuto")
        
        sleep(5)