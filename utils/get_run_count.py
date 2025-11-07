import sys
import os 
import itertools
from file_reader import get_runs_from_config

"""
gets the amount of runs for each config, REMOVING all other files!

run in main please

USAGE:
    from utils.get_run_count import get_run_count

    OR 

    python utils/get_run_count.py AA
"""

def get_run_count(config : str):
    return len(get_runs_from_config(config))

if __name__ == "__main__":
    try:
        print(get_run_count(sys.argv[1]))
    except Exception:
        for comb in itertools.product("ABCDEF", "ABCDEF"):
            config = "".join(comb)
            print(f"{config}: {get_run_count(config)} runs")
