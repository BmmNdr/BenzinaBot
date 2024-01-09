from time import sleep
import requests
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    
    latDistance = math.radians(lat2 - lat1)
    lonDistance = math.radians(lon2 - lon1)
    a = math.sin(latDistance / 2) * math.sin(latDistance / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lonDistance / 2) * math.sin(lonDistance / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

class openroute:
    def __init__(self, apiKey):
        self.baseUrl = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={apiKey}"
        
    def get_RoadDistance(self, start_lat, start_lon, end_lat, end_lon):
        url = self.baseUrl + f"&start={start_lon},{start_lat}&end={end_lon},{end_lat}"
        
        response = requests.get(url)
        data = response.json()
        
        distance = data["features"][0]["properties"]["summary"]["distance"]
        return distance
        
    def findBest(self, location, stations, quantity, consumption):
        minDist = 15 #km
        
        minId = None
        minPrice = None
        
        for imp in stations:
            dist = calculate_distance(location["latitude"], location["longitude"], imp["Latitudine"], imp["Longitudine"])
            
            if(dist <= minDist):
                roadDist = self.get_RoadDistance(location["latitude"], location["longitude"], imp["Latitudine"], imp["Longitudine"]) / 1000 #km
                
                roadCons = (consumption * roadDist) / 100
                
                totquantity = quantity + roadCons
                
                total = totquantity * imp["prezzo"]
                
                if(minPrice == None or total < minPrice):
                    minPrice = total
                    minId = imp["idImpianto"]
                    
                sleep(1.5) #to avoid exceeding the API limit (40 requests per minute)
                    
        return minId, minPrice