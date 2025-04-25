#!/usr/bin/env python
import itertools
import subprocess
import traceback
"""
executes a batch of assertiveness observers using the given count.
"""

possible_slots = "AB"
for comb in itertools.product(possible_slots, possible_slots):
    config = "".join(comb)
    
    try:
        subprocess.run(
            ["./assertiveness_observer.py", config],
        )
    except Exception:
        traceback.print_exc()
        break