import requests
from time import sleep
from telegramBot import telegramBot

naftaBot = telegramBot()

while(True):
    messages = naftaBot.getUpdates()
    
    for msg in messages:
        chat_id = msg["message"]["chat"]["id"]
        text = msg["message"]["text"]
        
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