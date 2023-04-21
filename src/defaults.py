"""A module containing all the default functions"""
import random


def prbl(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The probability is directy
    proportional to the given level."""
    random_num = random.random()
    return level > random_num

def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(1.6, 4.0) / 10
