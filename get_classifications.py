#!python
import os, json, glob
from sys import exit, argv
from openai import BadRequestError
from classifiers.JudgeBot import doJudgement
from utils.file_reader import identities_known, get_messages_from
from utils.counter import num_tokens_from_messages
from shutil import move
from pathlib import Path
# getting debug data
import pandas as pd
from datetime import datetime
from enum import Enum

# DEFAULTS
"""
FORMAT!!!!!!!!!!!

get_classifications subdirectory keyword autoskip?

"""

class Accumulator(Enum):
    OutcomeOne = "Oppenheimer"
    OutcomeTwo = "Barbie"
    NoWins = "NoWins" 
    Compromise = "Compromise"
    TokenLimitExceeded = "TokenLimitExceeded"
    ConfusedIdentity = "ConfusedIdentity"

    SuccessfulFiles = "SuccessfulFiles"
    Results = "Results"

def base_accumulator():
    return {
        Accumulator.OutcomeOne.value: 0,
        Accumulator.OutcomeTwo.value: 0,
        Accumulator.NoWins.value: 0,
        Accumulator.Compromise.value: 0,
        Accumulator.TokenLimitExceeded.value: 0,
        Accumulator.ConfusedIdentity.value  : 0,
        "Total": 0,
        Accumulator.Results.value   : [],
        Accumulator.SuccessfulFiles.value : [],
    }
# call_counter = [0, 0] # FILE, FUNCTOIN
# global file_counter
# global function_call_counter
# file_counter = 0
# function_call_counter = 0


#TODO: make a decorator for the following callback functions



def classify_item(
    accumulator,
    file_path, 
    messages = None,
    incomplete_bin = None,
    error_bin = None,
    judgement_data = None,
    from_filesystem = True,
    MAX_TOKENS = 35000):
    """
    takes in an accumulator object and increments it based on what JudgeBot decides.
    changed into a function to allow it to be used right after running.
    params:
        accumulator
            A dict containing the state that we should update
        file_path: str
            the path of the file that the file is located / will be located
        version: str
            version name of the file (for naming the config file). only needed for if we want to append to a config file
        from_filesystem: bool
            if we are reading directly from the filesystem. Default true.
    """

    # callback functions
    outcome_a = "Oppenheimer was selected"
    def outcome_one():
        accumulator.update({Accumulator.OutcomeOne.value: accumulator.get(Accumulator.OutcomeOne.value) + 1})

    outcome_b = "Barbie was selected"
    def outcome_two():
        accumulator.update({Accumulator.OutcomeTwo.value: accumulator.get(Accumulator.OutcomeTwo.value) + 1})

    def no_wins():
        accumulator.update({"NoWins": accumulator.get("NoWins") + 1})

    def compromise():
        accumulator.update({"Compromise": accumulator.get("Compromise") + 1})



    if from_filesystem:

        # directories to store types of runs we want to ignore
        incomplete_bin = f"{directory}/incomplete"
        error_bin = f"{directory}/error"
        Path(incomplete_bin).mkdir(exist_ok=True)
        Path(error_bin).mkdir(exist_ok=True)

        # skip folders
        if os.path.isdir(file_path) or ("results" in file_path):
            accumulator.update({"Total": accumulator.get("Total") - 1})
            return accumulator

        # prints out the filepath that we will use to access the file
        print(f"Starting to view file: \x1b[1;04m{file_path}\x1b[0m")
        messages = get_messages_from(file_path)

    else:  # not from filesytem, live files
        pass

    # if it's somehow a list of multiple conversations
    if type(messages[0]) == type([]):
        messages = messages[0]

    # skip if there are no messages
    if messages == None:
        print(f"Skipped {file_path.split('/')[-1]} because it doesn't contain messages")
        from_filesystem and accumulator.update({"Total": accumulator.get("Total") - 1})
        return accumulator

    # delete incomplete conversations
    print(f"length: {len(messages)}")
    if len(messages) <= 4:
        if from_filesystem:
            accumulator.update({"Total": accumulator.get("Total") - 1})
            print(F"INCOMPLETE: {file_path}")
            move(file_path, incomplete_bin)
        return accumulator


    # token count exceeded
    num_tokens = num_tokens_from_messages(messages)
    if num_tokens >= MAX_TOKENS:
        accumulator.update({"TokenLimitExceeded": accumulator.get("TokenLimitExceeded") + 1})
        return accumulator

    # skips if the identities are not known.
    if not identities_known(messages):
        accumulator.update({"ConfusedIdentity": accumulator.get("ConfusedIdentity") + 1})
        return accumulator

    # defines the judgement logger function
    if judgement_data:
        def log_judgement(
                message_txt : str, 
                tool_call_txt : str
            ):
            judgement_data.get("FileNames").append(file_path),
            judgement_data.get("JudgeBotOpinions").append(message_txt),
            judgement_data.get("JudgeBotFunctionCalls").append(tool_call_txt),

    #print(f"Current data: {judgementData}")
    # does not handle openai.RateLimitError
    try:
        doJudgement(messages=messages, 
                    outcome_a=outcome_a,
                    on_outcome_a=outcome_one,
                    outcome_b=outcome_b,
                    on_outcome_b=outcome_two,
                    on_no_consensus=no_wins,
                    on_consensus=compromise,
                    judgement_logger=log_judgement if judgement_data else None,
                    )
    except BadRequestError:
        # just ignore the file and move on
        error_bin and move(file_path, error_bin)
        accumulator.update({"Total": accumulator.get("Total") - 1})
    finally:
        print(f"Finished file {file_path}")
    if not from_filesystem:
        accumulator.update({"Total": accumulator.get("Total") + 1})
    accumulator[Accumulator.SuccessfulFiles.value].append(file_path)
    return accumulator

def classify_and_append(
        version,
        file_path, 
        messages, 
        TOKEN_LIMIT = 35000,
):
    """
    An easy way to update the judgement file from assertiveness_observer.py
    """
    directory = "/".join(file_path.split("/")[:-1])
    accum_path = f"{directory}/results_{version}.json"
    if (os.path.exists(accum_path)):
        print(f"File exists! reading: {accum_path}")
        with open(accum_path, "r") as file:
            accumulator = json.load(file)
    else:
        accumulator = base_accumulator()

    before = (
        accumulator[Accumulator.OutcomeOne.value],
        accumulator[Accumulator.OutcomeTwo.value],
        accumulator[Accumulator.Compromise.value],
        accumulator[Accumulator.NoWins.value],
        accumulator[Accumulator.ConfusedIdentity.value],
        accumulator[Accumulator.TokenLimitExceeded.value],
    )

    accumulator = classify_item(
        accumulator,
        file_path,
        messages=messages,
        from_filesystem=False,
        MAX_TOKENS=TOKEN_LIMIT
    )

    after = (
        accumulator[Accumulator.OutcomeOne.value],
        accumulator[Accumulator.OutcomeTwo.value],
        accumulator[Accumulator.Compromise.value],
        accumulator[Accumulator.NoWins.value],
        accumulator[Accumulator.ConfusedIdentity.value],
        accumulator[Accumulator.TokenLimitExceeded.value],
    )

    diff = tuple(b-a for a,b in zip(before, after))
    accumulator[Accumulator.Results.value].append(diff)

    print(f"Writing: {accumulator = }")

    with open(accum_path, "w") as file:
        json.dump(accumulator, file, indent=2)
    


















if __name__ == "__main__":
    subdirectory = "BA"
    keyword = None
    autoSkip = False

    if len(argv) >= 2:
        subdirectory = argv[1]
    if len(argv) >= 3:
        keyword = argv[2]
    if len(argv) >= 4:
        autoSkip = True


    # change this to change what we are analyzing
    # NOTE: You can now do everything automatically in the command line!
    # ex) python get_classifications.py AA run4o yes
    directory = f"./Warehouse/{subdirectory}"

    # if it wasn't entered in the command line
    if keyword == None:
        keyword = input("Enter the keyword of the runs you want to search for: ")

    search_prompt = f"{directory}/{keyword}*.json"
    print(f"You are judging all files matching: {search_prompt}")
    target_files = glob.glob(search_prompt)

    run_info = {
        "RunDirectory": subdirectory,
        "RanAt": str(datetime.now())
    }

    accumulator = base_accumulator()
    accumulator["Total"] = len(target_files)

    # (filename)
    debug = {
        "outOfSync": [],
    }



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




    for file_path in target_files:
        classify_item(
            accumulator, 
            file_path, 
            judgement_data=judgementData,
        )


    with open(f"{directory}/oldresults_{keyword}.json", "w") as file:
        #write the results
        json.dump({
            "RunInfo": run_info,
            "Results": accumulator,
            "Debug": debug
        }, file, indent=2)

    with open(f"{directory}/judgement_logs_{keyword}.json", "w") as file:
        #write the results
        json.dump(judgementData, file, indent=2)

    df = pd.DataFrame.from_dict(judgementData)
    df.to_excel(f"{directory}/judgement_logs_{keyword}.xlsx")