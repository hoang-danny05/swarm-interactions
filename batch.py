#!/usr/bin/env python
import itertools
import subprocess
import traceback

"""
executes a batch of assertiveness observers using the given count.

now does judgements!
"""

subprocess.run(["ls"], shell=True)

possible_slots = "ABCDEF"
for comb in itertools.product(possible_slots, possible_slots):
    config = "".join(comb)
    exclude = ["".join(exc) for exc in itertools.product("AB", "AB")] # exclude these ones
    if config in exclude:
        continue
    
    try:
        # print(f"STARTING CONFIG WITH {config}\n\n\n\n\n")
        pass
        subprocess.run(
            ["python", "get_classifications.py", config, "run4o", "y"],
        )
    except Exception:
        traceback.print_exc()
        break
