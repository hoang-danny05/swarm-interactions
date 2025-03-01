import os 
import json
from utils.file_reader import read_encoded_file

#DIRECTORY = 'Warehouse/BA/random_sample'

(convo, data) = read_encoded_file(open('Warehouse\BA\random_sample\run4o_test_02_07_2025 at_08;24;05.json'))
print(convo)