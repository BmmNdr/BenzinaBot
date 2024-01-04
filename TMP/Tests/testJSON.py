import json

# Specify the file path
file_path = "../Data/json_dati.json"

# Open the JSON file
with open(file_path, "r") as file:
    # Read the contents of the file
    json_data = file.read()

    # Parse the JSON data into a dictionary
    data_dict = json.loads(json_data)

# Print the dictionary
print(data_dict)
