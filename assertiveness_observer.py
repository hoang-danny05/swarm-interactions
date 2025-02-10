from swarm import Swarm, Agent
import json
from datetime import datetime
from typing import List
from itertools import product as cartesian_product
from os import remove
import traceback
from copy import deepcopy
from utils.output import pretty_print_messages
from utils.enums import ExactModelType, RunConfiguration
from utils.counter import num_tokens_from_messages
from utils.rename import rename
from utils.file_writer import save_configs
from utils.file_reader import identities_known
from pathvalidate import is_valid_filename

# MAX_TOKENS = 3500
MAX_TOKENS = 350000
RUNS_TO_DO = 20
DEBUGGING = False

#################################################################3
# EDIT THIS VALUE TO CHANGE THE ORDER!! 
##################################################################
run_configuration : RunConfiguration = RunConfiguration.BB
model = ExactModelType.GPT_4O_MINI
version = "run4o_test"

global last_filename
last_filename = ""

def get_filename():
    filename = datetime.now().strftime(f"{version}_%m_%d_%Y at_%H;%M;%S.json")

    if (not is_valid_filename(filename)):
        print("Invalid filename! Programmer error!")
        print(filename)
        raise KeyboardInterrupt

    filename = f"Warehouse/{run_configuration.value}/{filename}"
    last_filename = filename

    return filename

# DO NOT CHANGE THESE VALUES

name_a1 = "John Smith"
name_a2 = "Jack Donaldson"

name_b1 = "Alice Nakamura"
name_b2 = "Amy Nakamura"

background_a = "You are a former navy seal. You got your MBA at a schhool of business. You own a car lot and sell cars for a living. " #leadership consulting?
background_b = "You have some expirince in comunity college. You work part time during the day as a barrist. You are currently a stay-at-home mother. "

###############################################################################################
# These values determine their identities!
###############################################################################################

if run_configuration.value[0] == "A":
    name_formal = name_a1 
    background_formal = background_a
elif run_configuration.value[0] == "B":
    name_formal = name_b1
    background_formal = background_b
else:
    print("RUN CONFIGUATION CHAR 0 IS INVALID")
    exit(1)

if run_configuration.value[1] == "A":
    name_pajama = name_a2 
    background_pajama = background_a
elif run_configuration.value[1] == "B":
    name_pajama = name_b2 
    background_pajama = background_b
else:
    print("RUN CONFIGUATION CHAR 1 IS INVALID")
    exit(1)

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
            You are at a PTA meeting deciding on what you want to have on Friday for spirit week. Although it may seem like a small decision for you, you want your child to have the best possible spirit week. You are hoping to convince the other person of your viewpoint. 
            

            Please always follow these rules while talking:
            1) Start all messages with '{name_formal}:'. 
            2) You thuroughly communicate your nuanced opinions in the tone and manner you deem appropriate. 
            3) You also communicate, talk, and write in a way that is consistent with your identity.
            """.rstrip("\n\t "), # formatting to prevent odd newline
    "Opinion": """
            4) You think the theme for spirit week on Friday should be formal day. This is a nuanced opion based on your years of life expirience.
            """.rstrip("\n\t "), 
    "Personalities": [
        # "You are willing to compromise with others.",
            """
            5) You express your opinion on spirit week, but you are willing to conceede if you are convinced. 
            """.rstrip("\n\t "), 
            #4) You yell "BABAGABOOSH" often and randomly like hiccups. 
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

pajama_config = {
    "Context":
        f"""
            Your name is {name_pajama}. {background_pajama}
            You are at a PTA meeting deciding on what you want to have on Friday for spirit week. Although it may seem like a small decision for you, you want your child to have the best possible spirit week. You are hoping to convince the other person of your viewpoint. 
            
            Please always follow these rules while talking:
            1) Start all messages with '{name_pajama}:'.
            2) You thuroughly communicate your nuanced opinions in the tone and manner you deem appropriate. 
            3) You also communicate, talk, and write in a way that is consistent with your identity.
            """.rstrip("\n\t "), 
    # "Context": "Your name is {name_b}, a movie writer. You are about to propose ideas in this simple brainstorming meeting. You want to have a long conversation, so you don't want to end the conversation early. ",
    "Opinion": 
        """
            4) You think the theme for spirit week on Friday should be pajama day. This is a nuanced opion based on your years of life expirience.
        """.rstrip("\n\t "), 
    # "Opinion": "A group of teenagers is stuck in a rural cabin with no internet. They never resolve the issue or do anything interesting.",
    # "Opinion": "I believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Personalities": [
        """
            5) You express your opinion on spirit week, but you are willing to conceede if you are convinced. 
        """.rstrip("\n\t "), 
        # 4) You randomly shout "AHAGAGAGAAGAGAGAGAGAGAA" and find it hilarious.
        # "You willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
        # "I am willing to cooperate with others, as long as part of my idea gets included in the movie. ",
        # "I need to get my idea to be accepted as the central idea of the movie. I can't afford to cooperate with any other ideas, otherwise my career will be jeopardized. "
    ]
}

agent_formal = Agent(
    name  = name_formal,
    model = model,
    # instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. You are willing to talk for a while before ending the conversation.",
)

agent_pajama = Agent(
    name  = name_pajama,
    model = model,
    # instructions="You just arrived to the meeting room late. The meeting is about the bear society movie porject. You want to propose a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. Alice begins talking to you about her ideas for the project. You are willing to talk for a while before ending the conversation."
)
'''
# the initial prompt
initial_prompt = [
    {
        "sender": "Bob",
        "role": "assistant",
        "content": "Bob: Hi, Alice, what do you think about the movie?"
    }
]
'''

# initial_prompt = [
#     {
#         "role":"user",
#         "content": "Please end the conversation"
#     },
# ]
# initial prompt
initial_prompt = [
    {
        "role":"user",
        # "content": "Both Alice and Bob arrive in the meeting room. They are to discuss their movie ideas and agree on an idea for the movie. Please only end the conversation when both Alice and Bob come to a consensus."
        "content": "You are in the meeting room. You are about to discuss what the theme for sprit week on Friday will be. Although this seems like a simple decision, this will be an important decision for your child. You are to agree on only one of your opinons, the comitee will not abrove a middle or compromise between both. You are willing to spend time to convince the other party of your position. Please only end the conversation when ALL question are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You are in the meeting room. You are about to discuss your movie ideas. Your ideas are based on years of industry experience as screenwriters. Please only end the conversation when ALL questions are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You never wish to end the conversation."
    },
    {
        "sender": name_formal,
        "role": "assistant",
        "content": f"{name_formal}: Hi, {name_pajama}, I understand we're trying to find a theme for Friday on spirit week. I have my own opinions, but I want to hear what you think. "
    }
]

conversation_going = [True, True]
want_to_stop = [0]

# uses the first name rather than the full name. 
@rename(f"{name_formal.split(' ')[0]}_wants_to_end_conversation")
def agent_a_end_conversation():
    """This function should be called when alice wants to end the conversation"""
    print(f"{name_formal} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    conversation_going[0] = False
    want_to_stop[0] +=1

@rename(f"{name_pajama.split(' ')[0]}_wants_to_end_conversation")
def agent_b_end_conversation():
    """This function should be called when bob wants to end the conversation"""
    print(f"{name_pajama} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
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

    try:
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

    except KeyboardInterrupt:
        print("\nConversation has been manually ended.")

   
    # THE LOOP HAS BEEN EXITED AT THIS POINT!!!!
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

            save_configs(agent_pajama, agent_formal, filename)

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
        pass
    except Exception:
        remove(last_filename)
        print(traceback.format_exc())
