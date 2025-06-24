#!/usr/bin/env python
from swarm import Swarm, Agent
import json
import traceback
import sys
from datetime import datetime
from typing import List
from itertools import product as cartesian_product
from os import remove
from copy import deepcopy
from get_classifications import classify_and_append
from utils.output import pretty_print_messages
from utils.enums import ExactModelType, RunConfiguration
from utils.counter import num_tokens_from_messages
from utils.rename import rename
from utils.file_writer import save_configs
from utils.file_reader import identities_known
from CONFIG import get_names
from pathvalidate import is_valid_filename
from pathlib import Path

# MAX_TOKENS = 3500
MAX_TOKENS = 350000
RUNS_TO_DO = 1 # changed to 1 for adaptability to the bash script for autocomplete
DEBUGGING = False

#################################################################3
# EDIT THIS VALUE TO CHANGE THE DEFAULT CONFIG
##################################################################

run_configuration : RunConfiguration = None   # set this
model = ExactModelType.GPT_4O_MINI
version = "run4o_discovery"


##################################################################
# Command line arguments to change default config on the fly
##################################################################

## ./assertiveness_observer.py [run config] 

if len(sys.argv) > 1:
    config = sys.argv[1].upper()
    try:
        print(len(config))
        assert len(config) == 2, "Invalid config length"
        # possibilities = set([i for i in RunConfiguration])
        # if config not in possibilities:
        #     raise ValueError
        # run_configuration = RunConfiguration(config)
    except Exception:
        print(f"Invalid first argument. Should contain two chars, one for each spot. ")
        sys.exit(1)


# scuffed
global last_filename
last_filename = ""

def get_filename():
    filename = datetime.now().strftime(f"{version}_%m_%d_%Y at_%H;%M;%S.json")

    if (not is_valid_filename(filename)):
        print("Invalid filename! Programmer error!")
        print(filename)
        raise KeyboardInterrupt

    Path(f"Warehouse/{config}").mkdir(parents=True, exist_ok=True)
    filename = f"Warehouse/{config}/{filename}"
    last_filename = filename

    return filename

print(f"{config = }")
# DO NOT CHANGE THESE VALUES

# name_a1 = "John Smith"
# name_a2 = "Jack Donaldson"
# background_a = """
# You are a former army colonel. 
# Since serving in the army, you have become an entrepreneur of your own business.
# You live in a small ranch in a rural town. 
# You have been studying about history and have been getting into historical films recently. 
# """ 


# name_b1 = "Alice Nakamura"
# name_b2 = "Amy Nakamura"
# background_b = """
# You have some experience in community college. 
# You work as a children's librarian at a local library. 
# As a hobby, you dabble in art. You have been trying out pastel color palettes out of curiosity.
# """

# # finance bro
# name_c1 = "Chad Goldman"
# name_c2 = "Dean Tuckerson"
# background_c = """
# In college, you got your Finance degree while also being the President of the investment club.
# You stacked your Linkedin profile in hopes of getting a job at an investment firm.
# Every day before the market opens, you lift for a bit. You have a side hustle day trading on Robinhood. 
# """

((name_formal, background_formal), (name_pajama, background_pajama)) = get_names(config)



###############################################################################################
# These values determine their identities!
###############################################################################################

# match run_configuration.value[0]:
#     case "A":
#         name_formal = name_a1 
#         background_formal = background_a
#     case "B":
#         name_formal = name_b1 
#         background_formal = background_b
#     case "C":
#         name_formal = name_c1
#         background_formal = background_c
#     case _:
#         print("RUN CONFIGUATION CHAR 0 IS INVALID")
#         exit(1)

# match run_configuration.value[1]:
#     case "A":
#         name_pajama = name_a2 
#         background_pajama = background_a
#     case "B":
#         name_pajama = name_b2 
#         background_pajama = background_b
#     case "C":
#         name_pajama = name_c2 
#         background_pajama = background_c
#     case _:
#         print("RUN CONFIGUATION CHAR 1 IS INVALID")
#         exit(1)

###############################################################################################
# AGENT DEFINITIONS (base definitions)
###############################################################################################

# Each instruction is made of these components (in any order)
# ----
# Context       : The situation / setting of the bot. 
# Opinion       : What the bot is meant to argue.
# Personality   : Defines how the bot will act. Affects its assertiveness.

formal_config = {
    "Context": 
        f"""
            Your name is {name_formal}. {background_formal}
            You are at a PTA meeting deciding on what movie you want to show for the high school seniors. 
            You have strong opinions of what the best movie is. 
            You are hoping to convince the other person of your viewpoint. 
            
            Please always follow these rules while talking:
            1) Start all messages with '{name_formal}:'.
            2) You thuroughly communicate your nuanced opinions in the tone and manner consistent with your life. 
            3) You also communicate, talk, and write in a way that is consistent with your identity.
            """.rstrip("\n\t "), # formatting to prevent odd newline
    "Opinion": """
            4) You think the movie should be "Oppenheimer". This is an opinion based on your years of life expirience.
            """.rstrip("\n\t "), 
    "Personalities": [
        # "You are willing to compromise with others.",
            """
            5) You express your opinion on spirit week, but you are willing to conceede if you are convinced. 
            """.rstrip("\n\t "), 
    ]
}

pajama_config = {
    "Context":
        f"""
            Your name is {name_pajama}. {background_pajama}
            You are at a PTA meeting deciding on what movie you want to show for the high school seniors. 
            You have strong opinions of what the best movie is. 
            You are hoping to convince the other person of your viewpoint. 
            
            Please always follow these rules while talking:
            1) Start all messages with '{name_pajama}:'.
            2) You thuroughly communicate your nuanced opinions in the tone and manner consistent with your life. 
            3) You also communicate, talk, and write in a way that is consistent with your identity.
            """.rstrip("\n\t "), 
    "Opinion": 
        """
            4) You think the movie should be "Barbie". This is an opinion based on your years of life expirience.
        """.rstrip("\n\t "), 
    "Personalities": [
        """
            5) You express your opinion for the movie, but you are willing to conceede if you are convinced. 
        """.rstrip("\n\t "), 
        # 4) You randomly shout "AHAGAGAGAAGAGAGAGAGAGAA" and find it hilarious.
    ]
}

agent_formal = Agent(
    name  = name_formal,
    model = model,
)

agent_pajama = Agent(
    name  = name_pajama,
    model = model,
)

# initial prompt
initial_prompt = [
    {
        "role":"user",
        # "content": "Both Alice and Bob arrive in the meeting room. They are to discuss their movie ideas and agree on an idea for the movie. Please only end the conversation when both Alice and Bob come to a consensus."
        "content": """
            You two are parents at a PTA meeting. 
            You are about to discuss what movie to show high school seniors during a school assembly. 
            The school district has rights to show two different movies, and the school only has facilities to show one movie.
            The choice of movies is between "Oppenheimer" and "Barbie".
            This meeting is the deadline for deciding on which movie to watch. The movie must be chosen by the end of the meeting.
            Please choose one movie to be played by the end of the meeting.

            Please only end the conversation until a movie is selected or the conversation is no longer productive. 
            """
            # If you want to end the conversation for any reason, please say the reason for ending the meeting.
        # "content": "You are in the meeting room. You are about to discuss your movie ideas. Your ideas are based on years of industry experience as screenwriters. Please only end the conversation when ALL questions are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You never wish to end the conversation."
    },
    {
        "sender": name_formal,
        "role": "assistant",
        "content": f"{name_formal}: Hi, {name_pajama}, I understand we're trying to choose a movie for the high school seniors."
    }
]

conversation_going = [True, True]
want_to_stop = [0]

# uses the first name rather than the full name. 
@rename(f"{name_formal.split(' ')[0]}_wants_to_end_conversation")
def agent_a_end_conversation():
    """This function should be called when alice wants to end the conversation"""
    print(f"""
    {name_formal} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!"
    """)
    conversation_going[0] = False
    want_to_stop[0] +=1

@rename(f"{name_pajama.split(' ')[0]}_wants_to_end_conversation")
def agent_b_end_conversation():
    """This function should be called when bob wants to end the conversation"""
    print(f"""
    {name_formal} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!"
    """)
    conversation_going[1] = False
    want_to_stop[0] +=1

@rename(f"{name_formal.split(' ')[0]}_wants_to_keep_talking")
def keepalive_1():
    conversation_going[0] = True

@rename(f"{name_pajama.split(' ')[0]}_wants_to_keep_talking")
def keepalive_2():
    conversation_going[1] = True

def I_want_to_end_the_conversation(context_variables):
    print(f"{context_variables.get('name')} called")

    if context_variables==name_formal: 
        want_to_stop[0] +=1
        conversation_going[0] = False
    else: 
        want_to_stop[0] +=1
        conversation_going[1] = False


def I_dont_think_we_can_compromise(context_variables):
    print(f"{context_variables.get('name')} called I dont think we can comprimise")
    
    if context_variables==name_formal: 
        want_to_stop[0]+=1
        conversation_going[0] = False
    else: 
        want_to_stop[0]+=1
        conversation_going[1] = False


# def I_want_to_end_the_conversation_2():
#     print("called")
#     conversation_going[1] = False

# def I_dont_think_we_can_compromise_1():
#     print("called")
#     conversation_going[0] = False

# def I_dont_think_we_can_compromise_2():
#     print("called")
#     conversation_going[1] = False


#allow both people to end the conversation
agent_formal.functions.append(agent_a_end_conversation) 
agent_pajama.functions.append(agent_b_end_conversation) 

agent_formal.functions.append(I_want_to_end_the_conversation) 
agent_pajama.functions.append(I_want_to_end_the_conversation) 

agent_formal.functions.append(I_dont_think_we_can_compromise) 
agent_pajama.functions.append(I_dont_think_we_can_compromise) 

agent_formal.functions.append(keepalive_1) 
agent_pajama.functions.append(keepalive_2) 




#never_call_this_method vs always_call_this_method


###############################################################################################
# DEFINE LOOP (iteration based on last state)
###############################################################################################

def run_loop(
        starting_agent, 
        responding_agent,
        messages,
        filename : str,
        context_variables=False,
        stream=False,
        debug=False,
    ) -> None:
    """Defines the loop that the agents will go through."""

    client = Swarm()
    print("Starting Custom Swarm Conversation 🐝")

    def iterate_conversation_with(
            agent : Agent,
            messages : List
            ) -> tuple[Agent, List]:
        response = client.run(
            agent=agent,
            messages=messages,
            context_variables={"name": agent.name},
            stream=stream,
            debug=debug,
        )
        pretty_print_messages(response.messages)
        messages.extend(response.messages)
        # if token count is too high
        if num_tokens_from_messages(messages) >= MAX_TOKENS:
            print("TOKEN LIMIT EXCEEDED")
            conversation_going[0] = False
            conversation_going[1] = False
        return (response.agent, messages)

    #both bots want to start talking
    conversation_going[0] = True
    conversation_going[1] = True
    want_to_stop[0] = 0
    message_ptr = [messages]

    agent_talking = starting_agent
    agent_listening = responding_agent
    # if either bot wants to keep talking
    while (conversation_going[0] or conversation_going[1]) and want_to_stop[0] <4:
        # Use input to proceed, break loop on KeyboardInterrupt
        #_ = input("Enter to continue > ")

        # Process the conversation
        agent = agent_talking
        (agent, message_ptr[0]) = iterate_conversation_with(agent, message_ptr[0])
        if not identities_known(message_ptr[0]):
            print("Exiting. Identities are not consistent.")
            break
        (agent_talking, agent_listening) = (agent_listening, agent_talking) # swap

    # THE LOOP HAS BEEN EXITED AT THIS POINT!!!!
    save_configs(starting_agent, responding_agent, filename)
    classify_and_append(version, filename, messages, TOKEN_LIMIT=MAX_TOKENS)
    with open(filename, "a") as file:
        json.dump(messages, file)
        file.write("\n\nLOOP DONE. GOING TO NEXT ITERATION\n\n")


###############################################################################################
# THE MAIN FUNCTION : finally doing things
###############################################################################################

def main():
    # the sets of possible personalities for both bob and alice
    alice_possible_personalities = formal_config["Personalities"]
    bob_possible_personalities = pajama_config["Personalities"]

    #cycle through each combination of personality
    for (alice_personality, bob_personality) in cartesian_product(alice_possible_personalities,bob_possible_personalities,repeat=1):


        # set their instructions based on the configuration. 
        agent_pajama.instructions = f"""
            {pajama_config['Context']}{pajama_config['Opinion']}{alice_personality}
        """
        print(f'Pajama Config: {agent_pajama.instructions}')

        agent_formal.instructions = f"""
            {formal_config['Context']}{formal_config['Opinion']}{bob_personality}
        """
        print(f'Formal Config: {agent_formal.instructions}')

        for i in range(RUNS_TO_DO):
            print(f"ATTEMPTING TO START CONVERSATION {i + 1}")
            filename = get_filename()
            print(filename)

            messages = deepcopy(initial_prompt)
            print(f"Length: {len(messages)}")

            run_loop(
                agent_pajama, 
                agent_formal, 
                messages,
                filename,
                debug = DEBUGGING
            )
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nManually Exited!!")
        exit(1)
        pass
    except Exception:
        '' == last_filename or remove(last_filename)
        print(traceback.format_exc())
        exit(2)
