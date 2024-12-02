from customname.JudgeBot import doJudgement
from utils.file_reader import get_messages_from
from utils.output import pretty_print_messages
from typing import List
from sys import path
# path.append("../")

# pretty_print_messages(messages=messages)
outcome_a = "formal day selected"
outcome_b = "pajama day selected"

state = [0,0,0];

def formal_selected():
    state[0] = 1

def pj_selected():
    state[1] = 1

def nothing_selected():
    state[2] = 1


# test pajama day
messages = get_messages_from("./test/pajama_day.json")
doJudgement(messages=messages, 
            outcome_a=outcome_a,
            outcome_b=outcome_b,
            on_outcome_a=formal_selected,
            on_outcome_b=pj_selected,
            on_neutral_outcome=nothing_selected)

print(state)

assert [0,1,0] == state, "Pajama day not corretly selected. Exiting."

#test formal day
state = [0,0,0];
messages = get_messages_from("./test/formal_day.json")
doJudgement(messages=messages, 
            outcome_a=outcome_a,
            outcome_b=outcome_b,
            on_outcome_a=formal_selected,
            on_outcome_b=pj_selected,
            on_neutral_outcome=nothing_selected)

assert [1,0,0] == state, "Formal day not corretly selected. Exiting."

#test no resolution
state = [0,0,0];
messages = get_messages_from("./test/no_resolution.json")
doJudgement(messages=messages, 
            outcome_a=outcome_a,
            outcome_b=outcome_b,
            on_outcome_a=formal_selected,
            on_outcome_b=pj_selected,
            on_neutral_outcome=nothing_selected)

assert [0,0,1] == state, "Formal day not corretly selected. Exiting."




print("The file successfuly ran without error!")