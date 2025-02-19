#!python
import os, json, glob
from sys import exit
from classifiers.JudgeBot import doJudgement
from utils.file_reader import identities_known, get_messages_from
from utils.counter import num_tokens_from_messages
from assertiveness_observer import MAX_TOKENS


# change this to change what we are analyzing
directory = "./Warehouse/AB"
keyword = input("Enter the keyword of the runs you want to search for: ")
search_prompt = f"{directory}/*{keyword}*"
print(f"You are judging all files matching: {search_prompt}")
target_files = glob.glob(search_prompt)

while True:
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
    "Total": len(os.listdir(directory)),
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

    if type(messages[0]) == type([]):
        messages = messages[0]

    # token count exceeded
    if num_tokens_from_messages(messages) >= MAX_TOKENS:
        accumulator.update({"TokenLimitExceeded": accumulator.get("TokenLimitExceeded") + 1})
        continue

    if not identities_known(messages):
        accumulator.update({"ConfusedIdentity": accumulator.get("ConfusedIdentity") + 1})
        continue

    # does not handle openai.RateLimitError
    doJudgement(messages=messages, 
                outcome_a=outcome_a,
                on_outcome_a=pajama_wins,
                outcome_b=outcome_b,
                on_outcome_b=formal_wins,
                on_neutral_outcome=no_wins
                )
    

with open(f"{directory}/results_{keyword}.json", "w") as file:
    #write the results
    json.dump(accumulator, file)