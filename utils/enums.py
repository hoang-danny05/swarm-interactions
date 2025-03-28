from enum import Enum

class ModelType(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    O1_PREVIEW = "o1-preview"
    O1_MINI = "o1-mini"
    O3_MINI = "o3-mini"

# https://platform.openai.com/docs/models#current-model-aliases
class ExactModelType(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo-0125"
    GPT_4O_MINI = "gpt-4o-mini-2024-07-18"
    O1 = "o1-2024-12-17"
    O1_MINI = "o1-mini-2024-09-12"
    O3_MINI = "o3-mini-2025-01-31"

class StringEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class RunConfiguration(StringEnum):
    """
    An enumeration describing the running order of the assertiveness observer
    Char 0 determines who argues for FORMAL
    Char 1 determines who argues for PAJAMAS
    """
    AA = "AA"
    AB = "AB"
    BA = "BA"
    BB = "BB"