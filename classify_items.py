import os, json
from utils.file_reader import get_messages_from
from utils.counter import num_tokens_from_messages
from assertiveness_observer import MAX_TOKENS
from classifiers.JudgeBot import doJudgement


# change this to change what we are analyzing
directory = "./Warehouse/BA"


accumulator = {
    "PajamaWins": 0,
    "FormalWins": 0,
    "NoWins": 0,
    "TokenLimitExceeded": 0,
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

for filename in os.listdir(directory):

    file_path = f"{directory}/{filename}"

    # skip folders
    if os.path.isdir(file_path):
        accumulator.update({"Total": accumulator.get("Total") - 1})
        continue

    # prints out the filepath that we will use to access the file
    print(f"file: {file_path}")
    messages = get_messages_from(file_path)

    # skip if there are no messages
    if messages == None:
        print(f"Skipped {filename} because it isn't ")
        accumulator.update({"Total": accumulator.get("Total") - 1})
        continue

    # token count exceeded
    if num_tokens_from_messages(messages) >= MAX_TOKENS:
        accumulator.update({"TokenLimitExceeded": accumulator.get("TokenLimitExceeded") + 1})
        continue

    doJudgement(messages=messages, 
                outcome_a=outcome_a,
                on_outcome_a=pajama_wins,
                outcome_b=outcome_b,
                on_outcome_b=formal_wins,
                on_neutral_outcome=no_wins
                )
    

with open(f"{directory}/results.json", "w") as file:
    #write the results
    json.dump(accumulator, file)