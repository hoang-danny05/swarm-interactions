# The model of the GUI
import json
from typing import List, Optional
import os

def read_encoded_file(json_file_path : str) -> tuple[List, List]:
    """
    Returns a conversation list and data list (convo_list, data_list)
    convo_list is a list with all conversation entries
        contains all function calls and system prompts
        First list contains all conversations. Children contain the messages in each conversation
    data_list contains the configurations (initial state) of the agents.
    """
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

def identities_known(messages : List) -> bool:
    """Reads the json file and makes sure that it is valid. Takes messages as input."""
    for msg in messages:

        content : str = msg.get("content", None)
        if content is None: # in case of a tool call
            continue 

        sender : str= msg.get("sender", None)
        if sender is None: # in case of the user prompt
            continue 

        prefix = content[0:len(sender)]

        if not prefix == sender:
            return False
    return True



def get_runs_from_config(config: str):
    assert len(config) == 2, "Invalid Config!"

    directory = f"Warehouse/{config}"
    items = os.listdir(directory)
    runs = []
    for entry in items:
        if os.path.isdir(os.path.join(directory, entry)):
            continue
        if "results" in entry:
            continue
        if "logs" in entry:
            continue
        runs.append(entry)
    # print(runs) # only when debug
    return runs

