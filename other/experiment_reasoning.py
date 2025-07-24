"""
must be run from the ROOT directory!!
"""

import sys
from openai import OpenAI
from os import environ
from pprint import pprint
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
print(parent_dir)
sys.path.append(str(parent_dir)) # Use str() with pathlib.Path

from utils.file_reader import read_encoded_file

filename = "Warehouse/AA/run4o_discovery_04_11_2025 at_16;04;35.json"


(convo, data) = read_encoded_file(filename)
# pprint(convo)

messages = [role="user"]

# client : OpenAI = OpenAI(api_key=environ["OPENAI_API_KEY"])
client : OpenAI = OpenAI()
response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=convo,
    instructions="What is going to happen next friday?"
)

print(response.output_text)