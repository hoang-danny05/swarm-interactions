#!/usr/bin/env python
import itertools
import subprocess
import traceback
import os
import glob

"""
executes a batch of assertiveness observers using the given count.

now does judgements!
"""

#subprocess.run(["ls"], shell=True)

possible_slots = "ABCDEF"
for comb in itertools.product(possible_slots, possible_slots):
    config = "".join(comb)

    try:
        runs = glob.glob(f"./Warehouse/{config}/NEW*")
        for run in runs:
            print(run)
            path = run.split("/", 3)
            print(path)
            path[-1] = path[-1][4:]
            new_path = "/".join(path)
            print(new_path)
            os.rename(run, new_path)
    except Exception:
        traceback.print_exc()
        break
