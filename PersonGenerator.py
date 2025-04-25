import random

class PersonGenerator:
    age_classes = {
        "young_adult": {
            "age_range": (18, 30),
            "genders": ["man", "woman", "neither man or woman"],
            "educations": [
                "High school diploma", "Some college", "Associate's degree",
                "Bachelor's degree", "Currently enrolled in college"
            ],
            "occupations": [
                "Customer support associate", "Junior software developer",
                "Administrative assistant", "Research assistant", "Barista",
                "Retail associate", "Server at a restaurant", "Hotel front desk agent",
                "Freelance photographer", "Lyft driver", "Content creator (YouTube/TikTok)",
                "Pet sitter / Dog walker", "Aspiring musician", "Graphic designer",
                "Art student", "Indie game developer", "Nursing student", "Medical scribe",
                "EMT", "Dental assistant", "Apprentice electrician", "HVAC trainee",
                "Construction laborer", "Etsy shop owner", "Online reseller",
                "College student", "Tutor"
            ],
        },
        "middle_aged": {
            "age_range": (31, 60),
            "genders": ["man", "woman", "neither man or woman"],
            "educations": [
                "Bachelor's degree", "Master's degree", "Associate's degree",
                "Some college", "PhD", "Professional certification (e.g. PMP, CPA)"
            ],
            "occupations": [
                "Software engineer", "Accountant", "Human resources manager",
                "Operations analyst", "Project manager", "Real estate agent",
                "Plumber", "Electrician", "Truck driver", "Welder",
                "Maintenance supervisor", "Restaurant manager", "Hotel operations lead",
                "Senior customer service rep", "Nurse", "Radiology technician",
                "Physician assistant", "Pharmaceutical sales rep", "Lab technician",
                "Public school teacher", "Social worker", "Nonprofit director",
                "City planner", "Firefighter", "UX designer", "Writer/editor",
                "Marketing strategist", "Small business owner", "Startup founder",
                "Contract web developer", "Freelance consultant"
            ],
        },
        "elderly": {
            "age_range": (61, 85),
            "genders": ["man", "woman", "neither man or woman"],
            "educations": [
                "High school diploma", "Associate's degree", "Bachelor's degree",
                "Some college", "Master's degree"
            ],
            "occupations": [
                "Retired factory worker", "Retired civil engineer", "Retired nurse",
                "Retired military officer", "Retired postal worker", "Retired lawyer",
                "Retired school principal", "Retired business owner", "Substitute teacher",
                "Museum guide", "Community garden volunteer", "Library assistant",
                "Part-time bookkeeper", "Part-time business consultant",
                "Freelance historian", "Grant reviewer", "Ceramic artist", "Poet",
                "Amateur photographer", "Farmers market vendor",
                "Online handmade crafts seller", "Church treasurer",
                "Neighborhood watch captain", "Volunteer hospice coordinator"
            ],
        }
    }

    hobby_bank = {
        "studying history": [
            "You have been getting into historical films recently.",
            "You’ve started reading biographies of revolutionary leaders.",
            "You’ve been visiting local museums and historic landmarks.",
            "You’re fascinated by medieval warfare and tactics.",
            "You’ve been watching documentaries on ancient civilizations.",
            "You joined a historical reenactment group for the summer."
        ],
        "dabbling in art": [
            "You have been trying pastel color palettes out of curiosity.",
            "You recently bought a watercolor set to try landscapes.",
            "You’ve started following digital illustrators on social media.",
            "You’re exploring abstract art through mixed media.",
            "You took a beginner’s charcoal sketching class.",
            "You’ve been attending weekend figure drawing sessions."
        ],
        "gaming": [
            "You’ve started playing strategy games to challenge your mind.",
            "You’re part of a co-op team in an online RPG.",
            "You’ve been streaming retro games in your free time.",
            "You recently picked up a VR headset to try immersive gameplay.",
            "You’ve been designing your own tabletop campaign.",
            "You’re learning game modding and level design."
        ],
        "baking": [
            "You recently experimented with sourdough and made your first starter.",
            "You tried baking macarons and nailed the texture.",
            "You’ve been obsessed with perfecting your pie crust.",
            "You started a weekend ritual of baking banana bread.",
            "You’ve been testing gluten-free recipes for fun.",
            "You’re creating your own cookie recipe book."
        ],
        "gardening": [
            "You’re growing cherry tomatoes on your windowsill.",
            "You built a raised bed for growing herbs and lettuce.",
            "You started composting kitchen scraps for soil enrichment.",
            "You’re trying your hand at bonsai cultivation.",
            "You’ve been attracting pollinators with native plants.",
            "You’re tracking seasonal changes in your garden journal."
        ],
        "writing poetry": [
            "You joined an online poetry exchange group.",
            "You’ve been writing haikus about your daily routines.",
            "You’re compiling a chapbook of love poems.",
            "You took part in a 30-day poetry writing challenge.",
            "You’ve been exploring spoken word and open mic nights.",
            "You started journaling in verse to process emotions."
        ],
        "hiking": [
            "You recently tackled a new trail near your area.",
            "You’ve been collecting trail maps from state parks.",
            "You’re training for a multi-day backpacking trip.",
            "You’ve been geocaching on your local hikes.",
            "You took a nature photography class while hiking.",
            "You’re identifying wildflowers along the trails."
        ],
        "watching anime": [
            "You’ve been marathoning classic Studio Ghibli films.",
            "You’re catching up on the latest seasonal releases.",
            "You’ve been attending virtual anime conventions.",
            "You started learning Japanese through subtitled shows.",
            "You’re collecting figurines and art books.",
            "You’re rewatching old favorites with a new appreciation."
        ],
        "yoga": [
            "You’ve started going to morning yoga in the park.",
            "You’re following a 30-day flexibility challenge.",
            "You tried aerial yoga at a new studio.",
            "You’ve been exploring yoga philosophy through reading.",
            "You’re focusing on breathwork and mindfulness.",
            "You joined a virtual yoga community for support."
        ],
        "birdwatching": [
            "You spotted a rare finch last weekend.",
            "You’ve started logging bird sightings in a field journal.",
            "You’re learning to identify calls and songs by ear.",
            "You installed a bird feeder outside your window.",
            "You joined a local Audubon Society bird walk.",
            "You’re planning a trip to a bird migration hotspot."
        ]
    }


    def __init__(self, age_class_name=None):
        self.age_class_name = age_class_name or random.choice(list(self.age_classes.keys()))
        self.data = self.age_classes[self.age_class_name]

        self.age = random.randint(*self.data["age_range"])
        self.gender = random.choice(self.data["genders"])
        self.education = random.choice(self.data["educations"])
        self.occupation = random.choice(self.data["occupations"])
        self.living_type = self.assign_living_type()
        self.hobby, self.hobby_update = self.assign_hobby()

    def assign_living_type(self):
        if self.age_class_name == "young_adult":
            if "student" in self.occupation and "college" in self.education:
                return "dorm"
            elif "freelance" in self.occupation or "barista" in self.occupation or "retail" in self.occupation:
                return "small apartment"
            else:
                return random.choice(["small apartment", "shared apartment"])
        elif self.age_class_name == "middle_aged":
            if "manager" in self.occupation or "engineer" in self.occupation:
                return "house"
            else:
                return random.choice(["small apartment", "house"])
        elif self.age_class_name == "elderly":
            if "Retired" in self.occupation:
                return random.choice(["senior living apartment", "small house"])
            else:
                return random.choice(["condo", "small house"])
        return "unknown"

    def assign_hobby(self):
        hobby = random.choice(list(self.hobby_bank.keys()))
        interest = random.choice(self.hobby_bank[hobby])
        return hobby, interest

    def profile(self):
        return {
            "Age Class": self.age_class_name.replace("_", " ").title(),
            "Age": self.age,
            "Gender": self.gender,
            "Education": self.education,
            "Occupation": self.occupation,
            "Living Type": self.living_type,
            "Hobby": self.hobby,
            "Recent Hobby Update": self.hobby_update
        }


background_template = """
You are a {age} {profession}. You idenitfy as a {gender}.
You live in a {type_of_home}.
You have {education_background} background.
In your free time, you enjoy {hobby_or_interest}, recently {specific_aspect_of_hobby}
"""
# Example usage:
if __name__ == "__main__":
    person = PersonGenerator()
    profile = person.profile()

    background_filled = background_template.format(
    age=profile['Age'],
    gender=profile["Gender"],
    profession= profile['Occupation'],
    type_of_home=profile['Living Type'],
    education_background=profile["Education"],
    hobby_or_interest=profile["Hobby"],
    specific_aspect_of_hobby=profile["Recent Hobby Update"],
    )
    #print(person.profile())

    print(background_filled)