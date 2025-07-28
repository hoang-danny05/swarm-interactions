# clean incorrect files that did not write the conversation
import sys
import glob
import os

assert len(sys.argv) == 2, "Incorrect amount of arguments, please give config"

search_prompt = f"{sys.argv[1]}/*.json"
target_files = glob.glob(search_prompt)


for filename in target_files:
    if "results" in filename:
        continue

    with open(filename, "r") as file:
        line_count = 0
        while file.readline():
            line_count += 1
        if line_count == 4:
            print(f"\x1b[1;31mRemoving: {filename}")
            os.remove(filename)
