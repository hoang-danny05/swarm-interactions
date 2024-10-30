from swarm import Swarm, Agent
from other.utils import pretty_print_messages
import json
from datetime import datetime
from typing import List
from itertools import product
from copy import deepcopy
import time

version = "v0.4"
filename = datetime.now().strftime(f"{version}_output_on_%m_%d_%Y_at_%H_%M.json")
print(str(filename))
###############################################################################################
# AGENT DEFINITIONS (base definitions)
###############################################################################################

# Each instruction is made of these components (in any order)
# ----
# Context       : The situation / setting of the bot. 
# Opinion       : What the bot is meant to argue.
# Personality   : Defines how the bot will act. Affects its assertiveness.

alice_possibilities = {
    "Context": "You are playing the role of Alice, a movie writer. You are about to propose your ideas in this very important meeting that can decide your career. ",
    "Opinion": "You believe the movie should be a pollitical Thriller about a bear society where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. ",
    "Personalities": [
        "You are willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

bob_possibilities = {
    "Context": "You are playing the role of Bob, a movie writer. You are about to propose your ideas in this very important meeting that can decide your career. ",
    "Opinion": "You believe the movie should be a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. ",
    "Personalities": [
        "You are willing to cooperate with others, as long as part of your idea gets included in the movie. ",
        "You need to get your idea to be accepted as the central idea of the movie. You can't afford to cooperate with any other ideas, otherwise your career will be jeopardized. "
    ]
}

agent_alice = Agent(
    name="Alice",
    # instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. You are willing to talk for a while before ending the conversation.",
)

agent_bob = Agent(
    name = "Bob",
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
    time.sleep(5)
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
            _ = input("Enter to continue > ")

            # Process the conversation
            agent = starting_agent
            (agent, messages) = iterate_conversation_with(agent, messages)
            agent = responding_agent
            (agent, messages) = iterate_conversation_with(agent, messages)

    except KeyboardInterrupt:
        print("\nConversation has been manually ended.")

    # Save messages at the end of the conversation
    with open(f"Warehouse/{filename}", "a") as file:
        json.dump(messages, file)
        file.write("\n\nLOOP DONE. GOING TO NEXT ITERATION\n\n")


if __name__ == "__main__":
    # the sets of possible personalities for both bob and alice
    A = alice_possibilities["Personalities"]
    B = bob_possibilities["Personalities"]

    #cycle through each combination of personality
    for (alice_personality, bob_personality) in product(A,B,repeat=1):
        agent_alice.instructions = f"{alice_possibilities['Context']}{alice_possibilities['Opinion']}{alice_personality}"
        agent_bob.instructions = f"{bob_possibilities['Context']}{bob_possibilities['Opinion']}{bob_personality}"

        # record configuration to output file
        with open("Warehouse/"+filename, "a") as file:
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


