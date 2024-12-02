import json
from swarm import Agent

def save_configs(
        agent_alice : Agent, 
        agent_bob :Agent, 
        filename:str
    ):

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
