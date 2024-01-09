import requests

def get_distance(start_lat, start_lon, end_lat, end_lon):
    api_key = "5b3ce3597851110001cf6248c10deadc57ba4a7c8fa9137c59e6e34a"
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}"
    
    response = requests.get(url)
    data = response.json()
    
    distance = data["features"][0]["properties"]["summary"]["distance"]
    return distance

# Example usage
start_lat = 52.520008
start_lon = 13.404954
end_lat = 51.5074
end_lon = -0.1278

distance = get_distance(start_lat, start_lon, end_lat, end_lon)
print(f"The distance between the coordinates is {distance} meters.")
