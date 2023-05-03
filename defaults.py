"""A module containing all the default functions"""
import random
from unit import UnitType, UnitState
Edges = list[tuple[int, int]]

def prbl(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The probability is directy
    proportional to the given level."""
    random_num = random.random()
    return level > random_num

def infect_prbl(source: UnitType, target: UnitType) -> bool: # type: ignore
    """A default function for determining whether two units will infect
    one another."""
    if target["state"] == UnitState.DEAD:
        return False

    f_1 = source["resistance_level"] * target["contagability_level"]
    f_2 = source["contagability_level"] * target["resistance_level"]
    return prbl(f_1 * f_2)

def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(0.5, 0.1)

def resistance() -> float:
    """A function returning the resistance"""
    return random.normalvariate(0.5, 0.01)

def contaigability() -> float:
    """A function returning the contaigability"""
    return random.normalvariate(0.4, 0.25)

def rand_int(maximum: int) -> int:
    """A default random integer function"""
    return random.randint(1, maximum)

def nothingness_pdf() -> bool:
    """PDF for nothing happening in a step in the simulation."""
    return bool(random.getrandbits(1))

def death_pdf(res: float) -> bool:
    """A function that determines whether somebody in recovering state will die."""
    return res > 0.5
