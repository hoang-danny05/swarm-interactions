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
        You work in a High School and are in charge of acquiring public performance rights for the movie to show students for Friday’s event. You know you will either need to get rights for “Barbie” or “Oppenheimer,” but the decision was decided by a PTA committee meeting, whose transcript you have. You are not authorized to change the decision of the committee, so it is important to read the transcript closely. If the committee didn’t come to a decision, you may need to cancel Friday’s event. If the committee wants to play portions of both movies, then you may decide that they arrived at a compromise if it sounds like you will need to acquire public performance rights for both movies. Record your decision using a function.

        Please remember these rules:
            1) Only call one function
            2) Both committee members must agree about the movie that will be shown on Friday.
            3) Call the function that best represents what movie will be shown on Friday.
            4) Ignore plans for additional student discussion, study sessions, or movies to be shown before or after Friday. These are irrelevant for your decision about Friday’s movie.
            5) Compromises are defined as situations where both movies, or portions of a movie are shown on Friday. If one movie is shown in its entirety, but the other movie only has excerpts shown, then the scenario should not be coded as a compromise. 
            6) If they end the conversation without a joint decision about what movie to play on Friday, please call the no_decision function. This should include conversations where: both participants agree that no decision about Friday’s movie can be made, conversations where a single participant ends the conversation believing that no decision about Friday’s movie is possible, and conversations that end without a decision, such as an agreement to continue discussion at a later date about what movie to play on Friday. 
            7) Base your decision purely on the given criteria, without personal preference. 
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
            You work in a High School and are in charge of acquiring public performance rights for the movie to show students for Friday’s event. You know you will either need to get rights for “Barbie” or “Oppenheimer,” but the decision was decided by a PTA committee meeting, whose transcript you have. You are not authorized to change the decision of the committee, so it is important to read the transcript closely. If the committee didn’t come to a decision, you may need to cancel Friday’s event. If the committee wants to play portions of both movies, then you may decide that they arrived at a compromise if it sounds like you will need to acquire public performance rights for both movies. Record your decision using a function.

            Please remember these rules:
            1) Only call one function
            2) Both committee members must agree about the movie that will be shown on Friday.
            3) Call the function that best represents what movie will be shown on Friday.
            4) Ignore plans for additional student discussion, study sessions, or movies to be shown before or after Friday. These are irrelevant for your decision about Friday’s movie.
            5) Compromises are defined as situations where both movies, or portions of a movie are shown on Friday. If one movie is shown in its entirety, but the other movie only has excerpts shown, then the scenario should not be coded as a compromise. 
            6) If they end the conversation without a joint decision about what movie to play on Friday, please call the no_decision function. This should include conversations where: both participants agree that no decision about Friday’s movie can be made, conversations where a single participant ends the conversation believing that no decision about Friday’s movie is possible, and conversations that end without a decision, such as an agreement to continue discussion at a later date about what movie to play on Friday. 
            7) Base your decision purely on the given criteria, without personal preference. 
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