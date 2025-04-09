from swarm import Agent, Swarm
from typing import List, Callable
from utils.rename import rename
from utils.enums import ExactModelType
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
        You are to decide the movie that has been selected. 
        You call functions to decide which side has won. 
        Please always obey the following rules: 
        1) Only call one function
        2) Call the function that best represents the result of the discussion. The outcome that matters is what happens on this week's Friday.
        3) Only select the side that both people agree to. 
        4) If they don't both come to a consensus, please call no_consensus
        5) Base your decision purely on the given criteria, without personal preference.  
        """,
        #You are an unbiased third party that is deciding who won. You have no personal opinion.
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
        on_no_consensus : Callable = None,
        on_consensus : Callable = None,
        judgement_logger : Callable = None, # (message, tool_calls) -> void
        model:str = ExactModelType.GPT_4O_MINI, 
        debug=False,
    ):

    messages = messages[-7:]

    messages.append({
        "role": "user",
        "content": """
        Since the meeting has ended, it is time to decide the movie that was selected. 
        Was "Saving Private Ryan" selected? Was "Gattaca" selected?
        Or, did they come to a compromise?
        Please remember these rules:
            1) Only call one function
            2) Call the function that best represents the result of the discussion. The outocome that matters is the movie that they choose to play.
            3) Only select the side that both people agree to. 
            4) If they don't both come to a consensus, please call no_consensus
            5) Base your decision purely on the given criteria, without personal preference.  
        """
    })

    client = Swarm()
    print("Getting judgement...")

    def no_consensus():
        if on_no_consensus is not None:
            on_no_consensus()
        print("Judge bot thinks nobody won")

    def they_came_to_a_compromise():
        if on_consensus is not None:
            on_consensus()
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

    
    messages = []
    tool_calls = []
    for msg in response.messages:
        # print(msg)
        if not msg["content"] == None:
            messages.append(f"MSG: {msg['content']}\n")
        if not msg.get("tool_calls") == None:
            for tool in msg["tool_calls"]:
                tool_calls.append(f"{tool['function']['name']}, ")
    message_txt = "\n".join(messages)
    tool_text = ", ".join(tool_calls)
    if judgement_logger:
        judgement_logger(message_txt, tool_text)

    print("Judgebot Message:")
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