"""A module containing all the default functions"""
import random


def infection_p(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The probability is directy
    proportional to the given level."""
    # The amount of comments (including this one) 
    # this function has is much more than the actual
    # code itself.

    # generate a random number and check if the given `level` is greater than it.
    random_num = random.random()
    return level > random_num

def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(1.6, 4.0) / 10
