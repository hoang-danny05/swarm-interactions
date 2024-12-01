from swarm import Swarm, Agent
from utils.output import pretty_print_messages
import json
from datetime import datetime

###############################################################################################
# AGENT DEFINITIONS
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
# LOOP DEFINITION
###############################################################################################

def run_loop(
        starting_agent, 
        responding_agent,
        context_variables=False,
        stream=False,
        debug=False,
    ) -> None:
    """Defines the loop that the agents will go through."""
    client = Swarm()
    print("Starting Custom Swarm CLI 🐝")

    ###########
    # Gets the response of the starting agent
    ###########
    response = client.run(
        agent=agent_alice,
        messages = messages
    )
    # starting_message = response.messages[-1]["content"]
    messages.extend(response.messages)

    # add that message to the current messages

    # actual time to loop
    while True:

        # ask the user if they want to continue the loop
        try:
            user_continue = input("Enter to continue > ")
        except KeyboardInterrupt:
            break;

        # get a response
        response = client.run(
            agent=responding_agent,
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
        agent = response.agent

        ######################################################
        # Again, but get the starting_agent's response
        ######################################################

        # ask the user if they want to continue the loop
        try:
            user_continue = input("Enter to continue > ")
        except KeyboardInterrupt:
            break;

        # get a response
        response = client.run(
            agent=starting_agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            debug=debug,
        )

        pretty_print_messages(response.messages)
        messages.extend(response.messages)
        agent = response.agent
    
    # THE LOOP HAS BEEN EXITED AT THIS POINT!!!!
    with open(f"Warehouse/output_{datetime.now()}.json", "w") as file:
        json.dumps(messages, file)

if __name__ == "__main__":
    run_loop(agent_alice, agent_bob)




