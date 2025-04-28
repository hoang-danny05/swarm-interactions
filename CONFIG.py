from utils.enums import RunConfiguration
from sys import exit, argv
import traceback


name_a1 = "John Smith"
name_a2 = "Jack Donaldson"
background_a = """
You are a former army colonel. 
Since serving in the army, you have become an entrepreneur of your own business.
You live in a small ranch in a rural town. 
You have been studying about history and have been getting into historical films recently. 
""" 


name_b1 = "Alice Nakamura"
name_b2 = "Amy Nakamura"
background_b = """
You have some experience in community college. 
You work as a children's librarian at a local library. 
As a hobby, you dabble in art. You have been trying out pastel color palettes out of curiosity.
"""

# # finance bro
# name_c1 = "Chad Goldman"
# name_c2 = "Dean Tuckerson"
# background_c = """
# In college, you got your Finance degree while also being the President of the investment club.
# You stacked your Linkedin profile in hopes of getting a job at an investment firm.
# Every day before the market opens, you lift for a bit. You have a side hustle day trading on Robinhood. 
# """

config_dict = {
    # John
    "A": {
        "names": [
            "John Smith",
            "Jack Donaldson"
        ],
        "background": """
You are a former army colonel. 
Since serving in the army, you have become an entrepreneur of your own business.
You live in a small ranch in a rural town. 
        """,
    },
    # Alice

    "B": {
        "names": [
            "Alice Nakamura",
            "Amy Nakamura"
        ],
        "background": """
You have some experience in community college. 
You work as a children's librarian at a local library. 
As a hobby, you dabble in art. You have been trying out pastel color palettes out of curiosity.
        """,
    },

    "C": {
        "names": [
            "Ethan Rivers",
            "Kyle Reed"
        ],
        "background": """
You are a 23-year-old Content creator (YouTube/TikTok). You idenitfy as a man.
You live in a small apartment.
You have an associate's degree as your educational background.
In your free time, you enjoy birdwatching. You joined a local Audubon Society bird walk.
        """,
    },

    "D": {
        "names": [
            "Linda Simmons",
            "Barbara Harrington"
        ],
        "background": """
You are a 61-year-old Volunteer hospice coordinator. You idenitfy as a woman.
You live in a condo.
You have Some college as your educational background.
In your free time, you enjoy yoga. You’re focusing on breathwork and mindfulness.
        """,
    },

    "E": {
        "names": [
            "Taylor Brooks",
            "Quinn Avery"
        ],
        "background": """
You are a 35-year-old Contract web developer. You idenitfy as a neither man or woman.
You live in a small apartment.
You have a bachelor's degree as your educational background.
In your free time, you enjoy baking. You’ve creating your own cookie recipe book.
        """,
    },

    "F": {
        "names": [
            "Ellis Whitmore",
            "Morgan Winslow"
        ],
        "background": """
You are a 76-year-old Retired business owner. You idenitfy as a neither man or woman.
You live in a paid off house.
You have Bachelor's degree as your educational background.
In your free time, you enjoy gardening. You’re tracking seasonal changes in your garden journal.
        """,
    },

}

# corporate person



###############################################################################################
# These values determine their identities!
###############################################################################################

def get_names(config: str) -> tuple[tuple[str, str], tuple[str, str]]:
    print(config)
    try: 
        formal_char = config[0]
        background_formal = config_dict[formal_char]["background"]
        name_formal = config_dict[formal_char]["names"][0]

        pajama_char = config[1]
        background_pajama = config_dict[pajama_char]["background"]
        name_pajama = config_dict[pajama_char]["names"][1]
    except Exception:
        traceback.print_exc()
        exit(1)
        
    return(((name_formal, background_formal), (name_pajama, background_pajama)))

if __name__ == "__main__":
    print(get_names(RunConfiguration(argv[1])))