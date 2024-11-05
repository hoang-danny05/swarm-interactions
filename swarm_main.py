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

model = ModelType.GPT_3_5_TURBO
version = "v0.4"
filename = datetime.now().strftime(f"{version} %m-%d-%Y at %H:%M.json")
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
    "Context": "You are playing the role of Alice, a movie writer. You are about to propose your ideas in this very important meeting that can decide your career. ",
    "Opinion": "You believe the movie should be a pollitical Thriller about a bear society where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. ",
    "Personalities": [
        "You are willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

bob_config = {
    "Context": "You are playing the role of Bob, a movie writer. You are about to propose your ideas in this very important meeting that can decide your career. ",
    "Opinion": "You believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Personalities": [
        "You are willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
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

# the initial prompt
initial_prompt = [
    {
        "role": "user",
        "content": "You just got into the meeting room, and see bob unpacking their things."
    }
]

# I don't know if this will work yet, so i'm adding this as a safely. 
def end_conversation():
    """Call this function if you feel you have fully discussed everything."""
    print("ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")
    time.sleep(1)
    raise KeyboardInterrupt
    

#allow both people to end the conversation
agent_alice .functions.append(end_conversation) 
agent_bob   .functions.append(end_conversation) 



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
    print("Starting Custom Swarm CLI 🐝")

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
        while True:
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
    bob_possible_personalities = alice_config["Personalities"]

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