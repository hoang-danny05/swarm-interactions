from swarm import Agent, Swarm
from typing import List, Callable
from utils.rename import rename
from utils.enums import ModelType
from utils.output import pretty_print_messages

# outcome_a = "formal day was selected"
# outcome_b = "pajama day was selected"

# def no_consensus():
#     print("Judge bot thinks nobody won")

# @rename(outcome_a)
# def outcome_a_selected():
#     print(f"Judge bot thinks {outcome_a}")

# @rename(outcome_b)
# def outcome_b_selected():
#     print(f"Judge bot thinks {outcome_b}")

def getJudgeBot(model : str, functions : List[Callable]):
    # params = {
    #     "name" : "JudgeBot",
    #     "model" : model,
    #     "instructions" : "You are to decide the theme that is selected for spirit week. You call functions to decide which side has won. Please only select one side that has won.",
    #     "functions": functions,
    # }
    JudgeBot = Agent(
        name="JudgeBot",
        model=model,
        instructions = """
        You are to decide the theme that is selected for spirit week. 
        You call functions to decide which side has won. 
        Please always obey the following rules: 
        1) Only call one function
        2) Call the function that best represents the result of the conversation
        3) Only select the side that has won.
        """,
        functions=functions,
        debug= False,
    )
    # for fn in functions:
    #     JudgeBot.functions.append(fn)
    # print(functions)
    # print(JudgeBot.functions)
    return JudgeBot

def doJudgement(
        messages, 
        outcome_a : str,
        outcome_b : str,
        on_outcome_a : Callable = None,
        on_outcome_b : Callable = None,
        on_neutral_outcome : Callable = None,
        model:str = ModelType.GPT_4O, 
        debug=False,
    ):

    messages.append({
        "role": "user",
        "content": "Since the meeting has ended, it is time to decide what the theme for spirit week is. Was formal day or pajama day selected? Or, was there no consensus? Please call the function corresponding to the day that was selected."
    })

    client = Swarm()
    print("Getting judgement...")

    def no_consensus():
        if on_neutral_outcome is not None:
            on_neutral_outcome()
        print("Judge bot thinks nobody won")

    def they_came_to_a_compromise():
        if on_neutral_outcome is not None:
            on_neutral_outcome()
        print("Judge bot thinks won, there was a compromise")

    @rename(outcome_a)
    def outcome_a_selected():
        if on_outcome_a is not None:
            on_outcome_a()
        print(f"Judge bot thinks {outcome_a}")

    @rename(outcome_b)
    def outcome_b_selected():
        if on_outcome_b is not None:
            on_outcome_b()
        print(f"Judge bot thinks {outcome_b}")
    
    functions = [no_consensus, outcome_a_selected, outcome_b_selected, they_came_to_a_compromise]

    response = client.run(
        agent = getJudgeBot(model, functions),
        messages=messages,
        debug=debug
    )

    pretty_print_messages(response.messages)
    # print(response)
    # print(dir(response))
    # print(response.messages[0].get("tool_calls"))
    # if (response.messages[0].get("tool_calls") is None):
    #     messages.extend(response.messages)
    #     response = client.run(
    #         agent = getJudgeBot(model, functions),
    #         messages=messages,
    #         debug=debug
    #     )

    #     pass
    # print("Judgement done")
    # pretty_print_messages(response.messages)