from random import randint, random


def gen_int_without_repeats(num: int, minimum: int, maximum: int) -> int:
    """A function that generates a random integer that is NOT equal to `num`."""
    while True:
        random = randint(minimum, maximum)
        if random != num:
            return random

def return_prob(chance: float) -> bool:
    """A function that returns a probability given a chance. `x ∈ [0,1]`"""
    return chance < random()
