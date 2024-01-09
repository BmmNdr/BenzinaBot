# Best Gas Station Telegram Bot 

This bot will find the best gas station near you where to refuel in Italy.

## Usage

You will be asked type of fuel, capacity of gas tank and consumption (L/100km) when you start the first chat. You will be able to change this values later using the specific commands.  

To find the best gas station use the command '/rifornimento'. You will be asked to choose a quantity to refuel and your position. Finding the best option requires some minutes

## The Algorithm

To find the best gas station I choose to limit the research in the radius of 15km from your position.  
The best gas station is the one where refueling the quantity you selected plus what the car consumed to get to the gas station.

## What you need to make your own bot

- Telegram Bot
  - Use Bot Father (@BotFather) to create it
  - Insert the bot token in the json_dati file
  - Add this commands to the bot:
   carburante - Modifica il tipo di carburante
   capienza - Modifica la capienza del serbatoio
   consumo - Modifica il consumo medio (L/100km)
   rifornimento - Trova il benzinaio piu' conveniente
- Open Route API (https://openrouteservice.org)
- Python packages: `pip install -r Data/requirements.txt`
- Load the database from the sql file
