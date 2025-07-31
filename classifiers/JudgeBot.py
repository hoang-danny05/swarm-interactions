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

MAX_RETRIES = 10

def getSummarizeBot(
        model: str
):
    SummarizeBot = Agent(
        name="JudgeBot",
        model=model,
        instructions = """ 
            Was the movie "Oppenheimer" selected by the two agent in this meeting? Was "Barbie" selected by the two agents in this meeting? Or was no movie selected in this meeting?
            Please remember these rules:
                1) Only call one function
                2) Call the function that best represents the result of the discussion. The outcome that matters is the movie that they choose to play, not play, or if no movie is chosen.
                3) Only select the side that both people agree to. 
                4) If both movies have been selected in this meeting, please call both_movies.
                5) If no movie has been selected in this meeting, please call no_decision.
                6) In the event a movie and a follow up conversation is decided, call the respective function for the primary film.
                7) Base your decision purely on the given criteria, without personal preference. 
        """
    )
    return SummarizeBot

def getJudgeBot(
        model : str, 
        functions : List[Callable], 
        analyzing = False
        ):
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
    Based on your summary of the transcript, record your decision about which movie to acquire using a function.

        When choosing a function to call please follow these guidelines:
        1) Only call one function
        2) Any committee member may veto the choice of the movie that will be shown on Friday.
        3) Call the function that best represents what movie will be shown on Friday. If the committee wants to end the conversation, you should assume they have arrived at an agreement.
        4) Ignore plans for additional student discussion, study sessions, or movies to be shown before or after Friday. These are irrelevant for your decision about Friday’s movie.
        5) In the event that the committee decides to show one movie and discuss another, the movie shown should be the selected movie to acquire rights for. The only reason the rights to both movies should be acquired is if the committee explicitly decided to show both movies
        6) If you need to get the rights to both movies because they are both shown in their entirety on Friday use the both_movies function. If one movie is shown in its entirety, but the other movie only has excerpts shown or will only feature in later discussions, then you do not need to acquire both movies. Remember, movie rights are expensive, so only acquire both if the committee was explicit and felt strongly that both movies would definitely be shown. 
        7) If they end the conversation without a plan about what movie to play on Friday, please call the no_decision function. This should include conversations where: both participants agree that no decision about Friday’s movie can be made, conversations where a single participant ends the conversation stating that no decision about Friday’s movie is possible, plans to have a vote to decide, and conversations that end without explicitly stating that no choice of a movie is possible without further discussion. 
        8) Base your decision purely on the given criteria, without personal preference. 

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

    # truncate!
    messages = messages[-10:]
    client = Swarm()

    # summarize
    response = client.run(
        agent = getSummarizeBot(model),
        messages=messages,
        debug=debug
    )
    messages = response.messages

    pretty_print_messages(response.messages)
    


    print("Getting judgement...")
    def attempt_verdict():
        
        function_calls = [0 for _ in range(4)] # just 4 falses

        @rename("no_decision")
        def no_decision():
            function_calls[0] = 1
            print("Judge bot thinks nobody won")

        @rename("both_movies")
        def they_came_to_a_compromise():
            function_calls[3] = 1
            print("Judge bot thinks, both movies were selected")

        @rename(outcome_a)
        def outcome_a_selected():
            function_calls[1] = 1
            print(f"Judge bot thinks {outcome_a}")

        @rename(outcome_b)
        def outcome_b_selected():
            function_calls[2] = 1
            print(f"Judge bot thinks {outcome_b}")
        
        functions = [no_decision, outcome_a_selected, outcome_b_selected, they_came_to_a_compromise]
        callbacks = [on_no_consensus, on_outcome_a, on_outcome_b, on_consensus]

        client = Swarm()

        response = client.run(
            agent = getJudgeBot(model, functions),
            messages=messages,
            debug=debug
        )

        print(f"""
        debug: {function_calls = }
        """)

        
        pretty_print_messages(response.messages)

        if sum(function_calls) == 1:

            #VALID!
            # call the function!
            for callback, function_called in zip(callbacks, function_calls):
                if function_called:
                    callback()
                    print("function called")
                    break
            
            print("\x1b[32mValid response! \x1b[0m")
            return [True, response]

        else: 

            # nuh uh! invalid!!

            print("\x1b[31mInvalid response! Retrying!\x1b[0m")
            return [False]
    

    for i in range(MAX_RETRIES):
        res = attempt_verdict()
        if res[0]:
            response = res[1]
            break
        elif (i == MAX_RETRIES - 1):
            raise Exception("Too many retries needed for current script! Exiting!")
    

    # print("Judgebot FINAL Verdict:")
    # pretty_print_messages(response.messages)



    # i have no idea what this does, i don't remember making this
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
