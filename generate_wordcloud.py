#!/usr/bin/env python
import itertools
import os
import json
import sys
from utils.file_reader import get_runs_from_config, get_messages_from

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# TASK: generate word cloud of the different, unique words that each bot says

# 1) parse conversatoins and extract what a each person says

# 2) find unique words?

# 3) generate word cloud (use 3rd party library)



# lemmatization
# topic modeling and comparison
# word distributions

class freqencyDict():
    def __init__(self) -> None:
        self.full_dict = {}
        self.config_dict = {}

    def append(self, text:str):
        """
        Appends to the full dict and the single configuration dictionary.
        """
        print(f"ADDDING {text}, \n\nSPLIT: {text.split()}\n......")
        for word in text.split():
            word = word.rstrip(",!.?\"")
            word = word.lstrip(",!.?\"")
            if word in STOPWORDS:
                continue
            print(word)
            # add to dicts
            val = self.full_dict.get(word.lower(), 0)
            self.full_dict[word.lower()] = val + 1
            val = self.config_dict.get(word.lower(), 0)
            self.config_dict[word.lower()] = val + 1
        print("\n.....")
        #for key in temp_dict:
        #    self.full_dict[key] += temp_dict[key]
        #    self.config_dict[key] += temp_dict[key]

    def reset_config_dict(self):
        """
        Resets the current dictionary keeping track of the current configuration.
        """
        self.config_dict = dict()

    def generate_config_wordcloud(self, config):
        self.display_dict(self.config_dict)
        wc = WordCloud(width=500, height=400, margin=10, random_state=1, max_words=1000)
        wc.generate_from_frequencies(self.config_dict)

        plt.get_current_fig_manager().set_window_title(f"Wordcloud for config: {config}")
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        path = f"./wordclouds/{config}.png"
        wc.to_file(path)

    def generate_full_wordcloud(self):
        wc = WordCloud(width=500, height=400, margin=10, random_state=1, max_words=1000)
        wc.generate_from_frequencies(self.full_dict)

        plt.get_current_fig_manager().set_window_title("Summary Wordcloud")
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        path = f"./wordclouds/FULL.png"
        wc.to_file(path)

    def display_dict(self, dict):
        for k, v in dict.items():
            print(f"'{k}' ::::: '{v}'")






configs = "ABCDEF"


def main():
    # change in case you want to test
    warehouse_dir = "Warehouse"

    frequency_manager = freqencyDict()

    for conf in itertools.product(configs, configs):
        config = "".join(conf)

        frequency_manager.reset_config_dict()

        # for now, only do BD for debug purposes
        if not config == "DF":
            continue
        
        runs = get_runs_from_config(config)

        for run in runs:

            messages = get_messages_from(f"{warehouse_dir}/{config}/{run}")

            assert messages != None, "Invalid search directory!"

            for message in messages:
                print("===============================================")

                # ignore tools
                if message["role"] == "tool":
                    print("ingoring tool action")
                    continue 

                # ignore user prompt
                if message["role"] == "user":
                    print("ignoring user prompt.")
                    continue

                # record tool calls (distinct from tools)
                if message["content"] == None:

                    print(f"""
                    Tool call received:
                          {message['sender'] = }
                    """)

                    assert len(message["tool_calls"]) > 0, "Invalid tool call assumption"

                    for tool_call in message['tool_calls']:
                        assert tool_call["type"] == "function", "Invalid tool call assumption: all are functions"

                        func = tool_call["function"]["name"]
                        print(f"""
                        Call:
                            {tool_call = }
                            {tool_call["function"] = }
                            {func = }
                        """)
                        frequency_manager.append(func) 


                # process raw text messages
                else:
                    sender = message["sender"]
                    content = message["content"]

                    # trim sender prefix
                    content = content[len(sender)+1:]
                    print(sender)
                    print(content)
                    frequency_manager.append(content)
                print(message)

            # we only do this once for testing reasons
            #break

        frequency_manager.generate_config_wordcloud(config)
    frequency_manager.generate_full_wordcloud()


        


if __name__ == "__main__":
    main()
