import os 

from agents.AgentProfile import AgentProfile
from openai import OpenAI

class Agent:
    r"""Represents a singular instance of ChatGPT with a singular personality


    """
    def __init__(
            self,
            profile : AgentProfile
        ):
        self.profile : AgentProfile = profile

        self.client : OpenAI = OpenAI(
            api_key=os.environ("OPENAI_API_KEY"),
            )
        pass

    def send