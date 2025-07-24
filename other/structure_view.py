# Used to be scrub.py
# just to see the structure of a swarms "response.messages" object.
# meant to be run in the ROOT directory! move me there!
import os
import json
from pprint import pprint
from utils.file_reader import read_encoded_file

#DIRECTORY = 'Warehouse/BA/random_sample'

filename = "Warehouse/AA/run4o_discovery_04_11_2025 at_16;04;35.json"


(convo, data) = read_encoded_file(filename)
pprint(convo)