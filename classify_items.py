import os, json
from utils.file_reader import get_messages_from
from utils.counter import num_tokens_from_messages
from assertiveness_observer import MAX_TOKENS


directory = "./Warehouse/AA"

accumulator = {
    "PajamaWins": 0,
    "FormalWins": 0,
    "NoWins": 0,
    "TokenLimitExceeded": 0,
    "Total": len(os.listdir(directory)),
}

for filename in os.listdir(directory):
    file_path = f"{directory}/{filename}"
    if os.path.isdir(file_path):
        accumulator.update({"Total": accumulator.get("Total") - 1})
        continue

    # prints out the filepath that we will use to access the file
    print(f"file: {file_path}")
    messages = get_messages_from(file_path)

    # token count exceeded
    if num_tokens_from_messages(messages) >= MAX_TOKENS:
        accumulator.update({"TokenLimitExceeded": accumulator.get("TokenLimitExceeded") + 1})
        pass
    

with open(f"{directory}/results.json", "w") as file:
    #write the results
    json.dump(accumulator, file)