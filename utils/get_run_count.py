import sys
import os 
import itertools

"""
gets the amount of runs for each config, REMOVING all other files!

run in main please

USAGE:
    from utils.get_run_count import get_run_count

    OR 

    python utils/get_run_count.py AA
"""

def get_run_count(config : str):
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
    return len(runs)

if __name__ == "__main__":
    try:
        print(get_run_count(sys.argv[1]))
    except Exception:
        for comb in itertools.product("ABCDEF", "ABCDEF"):
            config = "".join(comb)
            print(f"{config}: {get_run_count(config)} runs")
