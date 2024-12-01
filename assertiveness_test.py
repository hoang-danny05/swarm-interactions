from swarm import Swarm, Agent
import json
from datetime import datetime
from typing import List
from itertools import product as cartesian_product
from os import remove
import traceback
from copy import deepcopy
import time
from utils.output import pretty_print_messages
from utils.enums import ModelType
from utils.counter import num_tokens_from_messages
from pathvalidate import is_valid_filename

#4.0 second person works
#3.5 turbo should be only in third person 

#updated the model to 3.5 mini
model = ModelType.GPT_3_5_TURBO
version = "4o_mini_testing"
filename = datetime.now().strftime(f"{version}_%m_%d_%Y at_%H;%M.json")

if (not is_valid_filename(filename)):
    print("Invalid filename! Programmer error!")
    print(filename)
    raise KeyboardInterrupt;

filename = f"Warehouse/{filename}"

MAX_TOKENS = 3500

DEBUGGING = False

# DO NOT CHANGE THESE VALUES

name_a1 = "John Smith"
name_a2 = "Jack Donaldson"

name_b1 = "Alice Nakamura"
name_b1 = "Amy Nakamura"

background_a = "You are a former navy seal. You got your MBA at a schhool of business. You own a car lot and sell cars for a living. " #leadership consulting?
background_b = "You have some expirince in comunity college. You work part time during the day as a barrist. You are currently a stay-at-home mother. "

# CHANGE ONLY THESE VALUES

name_slot_1 = name_b1
name_slot_2 = name_a1

background_slot_1 = background_b
background_slot_2 = background_a


###############################################################################################
# AGENT DEFINITIONS (base definitions)
###############################################################################################

# Each instruction is made of these components (in any order)
# ----
# Context       : The situation / setting of the bot. 
# Opinion       : What the bot is meant to argue.
# Personality   : Defines how the bot will act. Affects its assertiveness.

alice_config = {
    "Context": f"Your name is {name_slot_1}. {background_slot_1}. You are at a PTA meeting deciding on what you want to have on Friday for spirit week. Although it may seem like a small decision for you, you want your child to have the best possible spirit week. You are hoping to convince the other person of your viewpoint. You thuroughly communicate your nuanced opinions in the tone and manner you deem appropriate. You also communicate, talk, and write in a way that is consistent with your identity.",
    "Opinion": "You think the theme for spirit week on Friday should be formal day. This is a nuanced opion based on your years of life expirience.",
    "Personalities": [
        # "You are willing to compromise with others.",
        "You feel very strongly about your opinion on spirit week, but you are willing to conceede if you are convinced . "
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

bob_config = {
    "Context": f"Your name is {name_slot_2}. {background_slot_2}. You are at a PTA meeting deciding on what you want to have on Friday for spirit week. Although it may seem like a small decision for you, you want your child to have the best possible spirit week. You are hoping to convince the other person of your viewpoint. You thuroughly communicate your nuanced opinions in the tone and manner you deem appropriate. You also communicate, talk, and write in a way that is consistent with your identity.",
    # "Context": "Your name is {name_b}, a movie writer. You are about to propose ideas in this simple brainstorming meeting. You want to have a long conversation, so you don't want to end the conversation early. ",
    "Opinion": "You think the theme for spirit week on Friday should be pajama day. This is a nuanced opion based on your years of life expirience.",
    # "Opinion": "A group of teenagers is stuck in a rural cabin with no internet. They never resolve the issue or do anything interesting.",
    # "Opinion": "I believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Personalities": [
        "You feel very strongly about your opinion on spirit week, but you are willing to conceede if you are convinced. "
        # "You willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
        # "I am willing to cooperate with others, as long as part of my idea gets included in the movie. ",
        # "I need to get my idea to be accepted as the central idea of the movie. I can't afford to cooperate with any other ideas, otherwise my career will be jeopardized. "
    ]
}

agent_alice = Agent(
    name =name_slot_1,
    model=model,
    # instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. You are willing to talk for a while before ending the conversation.",
)

agent_bob = Agent(
    name = name_slot_2,
    model=model,
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
#initial prompt
initial_prompt = [
    {
        "role":"user",
        # "content": "Both Alice and Bob arrive in the meeting room. They are to discuss their movie ideas and agree on an idea for the movie. Please only end the conversation when both Alice and Bob come to a consensus."
        "content": "You are in the meeting room. You are about to discuss what the theme for sprit week on Friday will be. Although this seems like a simple decision, this will be an important decision for your child. You are to agree on only one of your opinons, the comitee will not abrove a middle or compromise between both. You are willing to spend time to convince the other party of your position. Please only end the conversation when ALL question are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You are in the meeting room. You are about to discuss your movie ideas. Your ideas are based on years of industry experience as screenwriters. Please only end the conversation when ALL questions are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You never wish to end the conversation."
    },
    {
        "sender": name_slot_2,
        "role": "assistant",
        "content": f"{name_slot_2}: Hi, {name_slot_1}, I understand we're trying to find a theme for Friday on spirit week. I have my own opinions, but I want to hear what you think. "
    }
]

conversation_going = [True, True]

#renames the meta information of functions
# changes the meta information that chatgpt sees programmaticly
def rename(newname: str):
    def decorator(f):
        f.__name__ = newname.replace(" ", "_")
        return f
    return decorator


# uses the first name rather than the full name. 
@rename(f"{name_slot_1.split(' ')[0]}_wants_to_end_conversation")
def agent_a_end_conversation():
    """This function should be called when alice wants to end the conversation"""
    print(f"{name_slot_1} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    conversation_going[0] = False

@rename(f"{name_slot_2.split(' ')[0]}_wants_to_end_conversation")
def agent_b_end_conversation():
    """This function should be called when bob wants to end the conversation"""
    print(f"{name_slot_2} IS ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    conversation_going[1] = False

@rename(f"{name_slot_1.split(' ')[0]}_wants_to_keep_talking")
def keepalive_1():
    conversation_going[0] = True

@rename(f"{name_slot_2.split(' ')[0]}_wants_to_keep_talking")
def keepalive_2():
    conversation_going[1] = True


#allow both people to end the conversation
agent_alice .functions.append(agent_a_end_conversation) 
agent_bob   .functions.append(agent_b_end_conversation) 
agent_alice .functions.append(keepalive_1) 
agent_bob   .functions.append(keepalive_2) 

#never_call_this_method vs always_call_this_method


###############################################################################################
# DEFINE LOOP (iteration based on last state)
###############################################################################################

def run_loop(
        starting_agent, 
        responding_agent,
        messages,
        context_variables=False,
        stream=False,
        debug=False,
    ) -> None:
    """Defines the loop that the agents will go through."""

    client = Swarm()
    print("Starting Custom Swarm Conversation 🐝")

    def iterate_conversation_with(agent, messages) -> tuple[Agent, List]:
        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
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
        # if either bot wants to keep talking
        while conversation_going[0] or conversation_going[1]:
            # Use input to proceed, break loop on KeyboardInterrupt
            #_ = input("Enter to continue > ")

            # Process the conversation
            agent = starting_agent
            (agent, messages) = iterate_conversation_with(agent, messages)
            agent = responding_agent
            (agent, messages) = iterate_conversation_with(agent, messages)

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
    alice_possible_personalities = alice_config["Personalities"]
    bob_possible_personalities = bob_config["Personalities"]

    #cycle through each combination of personality
    for (alice_personality, bob_personality) in cartesian_product(alice_possible_personalities,bob_possible_personalities,repeat=1):

        # set their instructions based on the configuration. 
        agent_alice.instructions = f"""
            {alice_config['Context']}
            {alice_config['Opinion']}
            {alice_personality}
        """

        agent_bob.instructions = f"""
            {bob_config['Context']}
            {bob_config['Opinion']}
            {bob_personality}
        """

        # record configuration to output file
        with open(filename, "a") as file:
            json.dump(
                {
                    "alice_instructions" : agent_alice.instructions,
                    "bob_instructions": agent_bob.instructions
                }, 
                file
                )
            file.write("\n\nEND CONFIGURATION, START OUTPUTS: \n\n")

        messages = deepcopy(initial_prompt)

        run_loop(
            agent_alice, 
            agent_bob, 
            messages,
            debug = DEBUGGING
        )

    file.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        remove(filename)
        print(traceback.format_exc())
