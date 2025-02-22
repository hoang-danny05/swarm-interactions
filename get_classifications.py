#!python
import os, json, glob
from sys import exit, argv
from classifiers.JudgeBot import doJudgement
from utils.file_reader import identities_known, get_messages_from
from utils.counter import num_tokens_from_messages
from assertiveness_observer import MAX_TOKENS
from shutil import move
from pathlib import Path
# getting debug data
import pandas as pd

# DEFAULTS
subdirectory = "AA"
keyword = None
autoSkip = False

if len(argv) >= 2:
    default_directory = argv[1]
if len(argv) >= 3:
    keyword = argv[2]
if len(argv) >= 4:
    autoSkip = True


# change this to change what we are analyzing
# NOTE: You can now do everything automatically in the command line!
# ex) python get_classifications.py AA run4o yes
directory = f"./Warehouse/{subdirectory}"
incomplete_bin = f"{directory}/incomplete"
Path(incomplete_bin).mkdir(exist_ok=True)

# if it wasn't entered in the command line
if keyword == None:
    keyword = input("Enter the keyword of the runs you want to search for: ")

search_prompt = f"{directory}/*{keyword}*.json"
print(f"You are judging all files matching: {search_prompt}")
target_files = glob.glob(search_prompt)

############# TEMPORARY
judgementData = {
    "FileNames": [],
    "JudgeBotOpinions": [],
    "JudgeBotFunctionCalls": [],
}

while not autoSkip:
    response = input(f"This will judge {len(target_files)} files. Are you sure?\n[y/n]:")
    if response.lower() == "y":
        break
    elif response.lower() == "n":
        exit(0)
    else:
        print("Invalid Response.")

accumulator = {
    "PajamaWins": 0,
    "FormalWins": 0,
    "NoWins": 0,
    "TokenLimitExceeded": 0,
    "ConfusedIdentity": 0,
    "Total": len(target_files),
}


# define outcome a and what to do when it happens
outcome_a = "pajama day was selected"
def pajama_wins():
    accumulator.update({"PajamaWins": accumulator.get("PajamaWins") + 1})

# define outcome b and what to do when it happens
outcome_b = "formal day was selected"
def formal_wins():
    accumulator.update({"FormalWins": accumulator.get("FormalWins") + 1})

# define what to do when nothing happens
def no_wins():
    accumulator.update({"NoWins": accumulator.get("NoWins") + 1})

for file_path in target_files:

    # skip folders
    if os.path.isdir(file_path):
        accumulator.update({"Total": accumulator.get("Total") - 1})
        continue

    # prints out the filepath that we will use to access the file
    print(f"file: {file_path}")
    messages = get_messages_from(file_path)

    # skip if there are no messages
    if messages == None:
        print(f"Skipped {file_path[-30:]} because it doesn't contain messages")
        accumulator.update({"Total": accumulator.get("Total") - 1})
        continue

    # if it's somehow a list of multiple conversations
    if type(messages[0]) == type([]):
        messages = messages[0]

    # delete incomplete conversations
    print(f"length: {len(messages)}")
    if len(messages) <= 4:
        print(F"INCOMPLETE: {file_path}")
        accumulator.update({"Total": accumulator.get("Total") - 1})
        move(file_path, incomplete_bin)
        continue


    # token count exceeded
    num_tokens = num_tokens_from_messages(messages)
    if num_tokens >= MAX_TOKENS:
        accumulator.update({"TokenLimitExceeded": accumulator.get("TokenLimitExceeded") + 1})
        continue

    # skips if the identities are not known.
    if not identities_known(messages):
        accumulator.update({"ConfusedIdentity": accumulator.get("ConfusedIdentity") + 1})
        continue

    # defines the judgement logger function
    def log_judgement(message_txt : str, tool_call_txt : str):
        judgementData.get("FileNames").append(file_path),
        judgementData.get("JudgeBotOpinions").append(message_txt),
        judgementData.get("JudgeBotFunctionCalls").append(tool_call_txt),

    print(f"Current data: {judgementData}")
    # does not handle openai.RateLimitError
    doJudgement(messages=messages, 
                outcome_a=outcome_a,
                on_outcome_a=pajama_wins,
                outcome_b=outcome_b,
                on_outcome_b=formal_wins,
                on_neutral_outcome=no_wins,
                judgement_logger=log_judgement,
                )
    

with open(f"{directory}/results_{keyword}.json", "w") as file:
    #write the results
    json.dump(accumulator, file)

with open(f"{directory}/judgement_logs_{keyword}.json", "w") as file:
    #write the results
    json.dump(judgementData, file)