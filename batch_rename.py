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
        items = glob.glob(f"./Warehouse/{config}/results*")
        for config in items:
            print(config)
            if "NEW" not in config:
                print("REMOVING:")
                os.remove(config)
                print(config)
    except Exception:
        traceback.print_exc()
        break
