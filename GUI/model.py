# The model of the GUI
import json

def read_encoded_file(json_file_path : str) -> (convo_list, data_list):
    convo_list = []
    data_list = []
    with open(json_file_path, 'r') as file:
        # Read all lines, assuming each JSON object starts with '{' on a new line
        for line in file:
            line = line.strip()
            if line.startswith("{"):  # Check if line begins with a JSON object
                try:
                    data = json.loads(line)
                    data_list.append(data)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON object: {e}")
            if line.startswith("["):
                try:
                    data = json.loads(line)
                    convo_list.append(data)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON object: {e}")
