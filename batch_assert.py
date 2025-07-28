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

    # Add any runs you want to exclude in this array ex) "AA"
    exclude = []
    # exclude = ["".join(exc) for exc in itertools.product("AB", "AB")] # exclude these ones
    if config in exclude:
        continue
    
    try:
        subprocess.run(
            ["python", "assertiveness_observer.py"],
        )
    except Exception:
        traceback.print_exc()
        break
