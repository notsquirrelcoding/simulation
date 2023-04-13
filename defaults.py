"""A module containing all the default functions"""
import random


def infection_p(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The way this default function works
    is by generating a random number in `[0, 1]`"""
    random_num = random.random()
    return level > random_num

def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(1.6, 4.0)
