#!/bin/bash
python assertiveness_observer.py cc &&
python assertiveness_observer.py cb &&
python assertiveness_observer.py ca && 
python assertiveness_observer.py ac &&
python assertiveness_observer.py bc 
# classifies them all
# python get_classifications.py AA run4o y &&
# python get_classifications.py AB run4o y &&
# python get_classifications.py BA run4o y &&
# python get_classifications.py BB run4o y