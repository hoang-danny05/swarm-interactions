#!/usr/bin/env python
import itertools
import subprocess
import traceback
from utils.get_run_count import get_run_count

"""
executes a batch of assertiveness observers using the given count.

now does judgements!

will do enough runs to get to the MINIMUN_RUNS
"""

MINIMUM_RUNS = 70


subprocess.run(["ls"], shell=True)

possible_slots = "ABCDEF"
for comb in itertools.product(possible_slots, possible_slots):
    config = "".join(comb)

    # Add any runs you want to exclude in this array ex) "AA"
    exclude = []
    # exclude = ["".join(exc) for exc in itertools.product("AB", "AB")] # exclude these ones
    if config in exclude:
        continue
    
    # see if the run count is low enough to do the runs
    run_count = get_run_count(config)
    if run_count > MINIMUM_RUNS:
        continue    
    runs_to_do = MINIMUM_RUNS - run_count

    try:
        subprocess.run(
            ["python", "assertiveness_observer.py", config, str(runs_to_do)],
        )
    except Exception:
        traceback.print_exc()
        break
