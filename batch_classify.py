#!/usr/bin/env python
import itertools
import subprocess
import traceback
from utils.get_run_count import get_run_count

"""
executes a batch of assertiveness observers using the given count.

now does judgements!
"""

#subprocess.run(["ls"], shell=True)

possible_slots = "ABCDEF"
for comb in itertools.product(possible_slots, possible_slots):
    config = "".join(comb)

    # Add any runs you want to exclude in this array ex) "AA"
    exclude = ["AA", "AB", "BA", "CA", "CB", "CC", "FF"]
    # exclude = ["".join(exc) for exc in itertools.product("AB", "AB")] # exclude these ones
    if config in exclude:
        continue
    
    # skip the runs which don't have new runs
    if get_run_count(config) != 100:
        continue

    
    try:
        # print(f"STARTING CONFIG WITH {config}\n\n\n\n\n")
        # print(config)
        subprocess.run(
            ["python", "get_classifications.py", config, "run4o", "y"],
        )
    except Exception:
        traceback.print_exc()
        break
