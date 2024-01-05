import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    
    latDistance = math.radians(lat2 - lat1)
    lonDistance = math.radians(lon2 - lon1)
    a = math.sin(latDistance / 2) * math.sin(latDistance / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lonDistance / 2) * math.sin(lonDistance / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Example usage
lat1 = 40.7128
lon1 = -74.0060
lat2 = 37.7749
lon2 = -122.4194

#coord1 = (40.7128, -74.0060)  # Latitude and Longitude of New York City
#coord2 = (37.7749, -122.4194)  # Latitude and Longitude of San Francisco


distance = calculate_distance(lat1, lon1, lat2, lon2)
print(f"The distance between the coordinates is {distance} kilometers.")
