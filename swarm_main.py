from swarm import Swarm, Agent
from other.utils import pretty_print_messages
import json
from datetime import datetime
from typing import List

###############################################################################################
# AGENT DEFINITIONS (base definitions)
###############################################################################################

# client = Swarm()

agent_alice = Agent(
    name="Alice",
    instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators. You are willing to talk for a while before ending the conversation.",
)

agent_bob = Agent(
    name = "Bob",
    instructions="You just arrived to the meeting room late. The meeting is about the bear society movie porject. You want to propose a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. Alice begins talking to you about her ideas for the project. You are willing to talk for a while before ending the conversation."

)

# the initial prompt
messages = [
    {
        "role": "user",
        "content": "You just got into the meeting room, and see bob unpacking their things."
    }
]

# I don't know if this will work yet, so i'm adding this as a safely. 
def end_conversation():
    """Call this function if you feel you have fully discussed everything."""
    print("ENDING CONVERSATION!!!!!!!!!!!!!!!!!!!!!")

#allow both people to end the conversation
agent_alice .functions.append(end_conversation) 
agent_bob   .functions.append(end_conversation) 


# with open("output.txt", "w") as file:
#     json.dump(response.messages, file)

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

    #define a step for a certain user. 
    def iterate_conversation_with(agent, messages) -> tuple[Agent, List]:
        """
        Used multiple times in the while loop. 
        iterates the messages with the input agent. 
        """
        # get a response
        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            debug=debug,
        )

        # i removed stream implementation here. If we end up doing streams, return to swarms.
        pretty_print_messages(response.messages)
        # update the conversation
        messages.extend(response.messages)
        # in case they switch
        return (response.agent, messages)



    # actual time to loop
    while True:

        # ask the user if they want to continue the loop
        try:
            _ = input("Enter to continue > ")
        except KeyboardInterrupt:
            break;

        # we still manually set the agent. We will soon experiment with allowing the AI figure out when to swap agents.
        agent = starting_agent
        (agent, messages) = iterate_conversation_with(agent, messages)
        agent = responding_agent
        (agent, messages) = iterate_conversation_with(agent, messages)

   
    # THE LOOP HAS BEEN EXITED AT THIS POINT!!!!
    with open(f"Warehouse/output_{datetime.now()}.json", "w") as file:
        json.dump(messages, file)

if __name__ == "__main__":
    run_loop(agent_alice, agent_bob, messages)




