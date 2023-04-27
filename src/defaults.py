"""A module containing all the default functions"""
import random

def prbl(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The probability is directy
    proportional to the given level."""
    random_num = random.random()
    return level > random_num

def infect_prbl(a: float, b: float) -> bool:
    """A default function for determining whether two units will infect
    one another."""
    return a > b

def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(0.5, 0.0001)

def resistance() -> float:
    """A function returning the resistance"""
    return random.normalvariate(0.6, 0.25)

def contaigability() -> float:
    """A function returning the contaigability"""
    return random.normalvariate(0.4, 0.25)

def rand_int(maximum: int) -> int:
    """A default random integer function"""
    return random.randint(1, maximum)

def nothingness_pdf() -> float:
    """PDF for nothing happening in a step in the simulation."""
    return random.random()
