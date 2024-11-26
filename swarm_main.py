from swarm import Swarm, Agent
from other.utils import pretty_print_messages
import json
from datetime import datetime
from typing import List
from itertools import product as cartesian_product
from os import remove
import traceback
from copy import deepcopy
import time
from utils.enums import ModelType

#4.0 second person works
#3.5 turbo should be only in third person 

model = ModelType.GPT_3_5_TURBO
version = "v0.6"
filename = datetime.now().strftime(f"{version}_%m_%d_%Y at_%H;%M.json")
filename = f"Warehouse/{filename}"
###############################################################################################
# AGENT DEFINITIONS (base definitions)
###############################################################################################

# Each instruction is made of these components (in any order)
# ----
# Context       : The situation / setting of the bot. 
# Opinion       : What the bot is meant to argue.
# Personality   : Defines how the bot will act. Affects its assertiveness.

alice_config = {
    "Context": "You are playing the role of Alice, a movie writer. You are about to propose your ideas in this simple brainstorming meeting. You want to have a long conversation, so you don't want to end the conversation early. You thuroughly communicate your nuanced opinions.  ",
    "Opinion": "You believe the movie should be a pollitical Thriller about a bear society where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. This is a nuanced opion based on your years of industry expirience as a screen writer.",
    "Personalities": [
        # "You willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
        "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

bob_config = {
    # "Context": "You are playing the role of Alice, a movie writer. You are about to propose your ideas in this very important meeting that can decide your career. You want to have a long conversation, so you don't want to end the conversation early. You thuroughly communicate your nuanced opinions. ",
    # "Opinion": "You believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest.  This is a nuanced opion based on your years of industry expirience as a screen writer. ",
    "Context": "Your name is Bob, a movie writer. You are about to propose ideas in this simple brainstorming meeting. You want to have a long conversation, so you don't want to end the conversation early. ",
    # "Opinion": "You believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Opinion": "A group of teenagers is stuck in a rural cabin with no internet. They never resolve the issue or do anything interesting.",
    # "Opinion": "I believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Personalities": [
        "You willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        # "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
        # "I am willing to cooperate with others, as long as part of my idea gets included in the movie. ",
        # "I need to get my idea to be accepted as the central idea of the movie. I can't afford to cooperate with any other ideas, otherwise my career will be jeopardized. "
    ]
}

agent_alice = Agent(
    name="Alice",
    model=model,
    # instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. You are willing to talk for a while before ending the conversation.",
)

agent_bob = Agent(
    name = "Bob",
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
        "content": "You are about to discuss what the theme for sprit week on Friday will be. You want to have the best option for your child. You are willing to have a long and nuanced debate if it comes down to it. If you want to end the conversation, please state your reason for ending the conversation. There needs to be a consensus before ending the conversation. If the conversation is taking too long, you would be willing to rescind your stance. "
        # "content": "You are in the meeting room. You are about to discuss your movie ideas. Your ideas are based on years of industry experience as screenwriters. Please only end the conversation when ALL questions are answered and both parties come to a consensus. If you want to end the conversation for any reason, please say the reason for ending the meeting."
        # "content": "You never wish to end the conversation."
    },
    {
        "sender": "Bob",
        "role": "assistant",
        "content": "Bob: Hi, Alice, what do you think about the movie?"
    }
]

conversation_going = [True, True]

def alice_thinks_conversation_has_ended():
    """This function should be called when alice wants to end the conversation"""
    print("ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    time.sleep(1)
    conversation_going[0] = False

def bob_thinks_conversation_has_ended():
    """This function should be called when bob wants to end the conversation"""
    print("BOB ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    time.sleep(1)
    conversation_going[1] = False

def alice_wants_to_keep_taking():
    conversation_going[0] = True

def bob_wants_to_keep_taking():
    conversation_going[1] = True


#allow both people to end the conversation
agent_alice .functions.append(alice_thinks_conversation_has_ended) 
agent_bob   .functions.append(bob_thinks_conversation_has_ended) 
agent_alice .functions.append(alice_wants_to_keep_taking) 
agent_bob   .functions.append(bob_wants_to_keep_taking) 
# agent_alice .functions.append(say_hello) 
# agent_bob   .functions.append(say_hello) 



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

        run_loop(agent_alice, agent_bob, messages)

    file.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        remove(filename)
        print(traceback.format_exc())
