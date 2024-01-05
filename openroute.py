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
    def __init__(self):
        self.apiKey = "5b3ce3597851110001cf6248f9f6a7e9b0d64f1fae6e7b7b0e3e4c2f"
        
    def findBest(self, location, impianti):
        minDist = 30
        
        nearest = []
        
        for imp in impianti:
            dist = calculate_distance(location["latitude"], location["longitude"], imp[8], imp[9])
            
            if(dist <= minDist):
                nearest.append(imp)
                
        for imp in nearest:
            print(imp)