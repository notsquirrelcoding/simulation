import random

"""A module containing all the default functions"""

def default_infection_p(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The way this default function works
    is by generating a random number in `[0, 1]`"""
    random_num = random.random()
    return level > random_num


