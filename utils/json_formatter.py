# json format
# let capitalized words be forms of data later defined
# let types ending with ! be temporary values that are defined by swarm_main

#     {
#         base_configs : {
#             initial_prompt!,
#             alice_config!,
#             bob_config!
#         }
#         iterations : [
#             ITERATION_DATA...
#         ]
#     }

# ITERATION_DATA = {
#     specific_config: {
#         alice_personality!,
#         bob_personality!
#     },
#     messages!
# }

import json

def write_base_configs_to(filename, general_config):
    """
    Creates a file based on the filename. 
    """
    init_obj = {
        "base_configs" : general_config,
        "iterations" : []
    }
    with open(filename, "w") as file:
        json.dump(init_obj, file)


def add_iteration_to(filename, iteration_data):
    """
    Adds an iteration to a json file. Assumes the file was created by write_base_configs_to
    """

    with open(filename, "a+") as file:
        data = json.load(file)

        iterations_list = data["iterations"]
        iterations_list.append(iteration_data)
        data["iterations"] = iterations_list

        json.dump(data, filename)

