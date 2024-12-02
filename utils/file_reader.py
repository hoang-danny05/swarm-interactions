# The model of the GUI
import json
from typing import List, Optional

def read_encoded_file(json_file_path : str) -> tuple[List, List]:
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
    return (convo_list, data_list)

def get_messages_from(file_path : str) -> Optional[List]:
    """
    Tries to read an output file and returns the messages JSON object 
    
    Does this by skipping lines that are invalid json
    """
    with open(file_path, "r") as file:
        for line in file:
            # remove whitespace
            line = line.strip();

            #skip non-message objects
            if not line.startswith("["):
                continue
                
            # try to process messages
            try:
                return json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON object: {e}")
    
    #In the case it does not exist
    return None
