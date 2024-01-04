import json
import os
from datetime import datetime

# Specify the file path
file_path = os.getcwd() + "/Data/json_dati.json"

# Open the JSON file
with open(file_path, "r") as file:
    # Read the contents of the file
    json_data = file.read()

    # Parse the JSON data into a dictionary
    data_dict = json.loads(json_data)

# Print the dictionary
data_dict["date"] = datetime.today().strftime('%Y-%m-%d')

with open(file_path, "w") as outfile:
    json.dump(data_dict, outfile)