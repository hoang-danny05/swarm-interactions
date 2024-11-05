from typing import Dict, List, Optional
from types.enums import ModelType

class AgentProfile():
    r""" Acts as settings that can be applied to an agent.

    Args:
            name (str): The name of the agent.
            relationship_prompt (str): The prompt to be given that defines 
                the bot's relationship with its partner
            model (optional[str]): The LLM model to be used.
    """

    def __init__(
        self,
        name: str,
        relationship_prompt: str,
        model: Optional[str] = ModelType.GPT_3_5_TURBO
    ) -> None:

        self.name = name
        self.relationship_prompt = relationship_prompt
        self.model : Optional[str] = model