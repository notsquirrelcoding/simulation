"""A module containing all the default functions"""
import random
from typing import List, Tuple
from unit import UnitType, UnitState
Edges = list[tuple[int, int]]


def pdf(level: float) -> bool:
    """A function determining whether or not a unit has been infected, 
    given it's vulnreability level. The probability is directy
    proportional to the given level."""
    random_num = random.random()
    return level > random_num


def infect_pdf(source: UnitType, target: UnitType) -> bool:  # type: ignore
    """A default function for determining whether two units will infect
    one another."""
    if target["state"] != UnitState.HEALTHY:
        return False
    if source["state"] == UnitState.HEALTHY:
        return False

    return one_in_n_prbl(10)


def normal_random() -> float:
    """A function that returns a random number """
    return random.normalvariate(0.5, 0.1)


def resistance() -> float:
    """A function returning the resistance"""
    return random.normalvariate(0.9, 0.01)


def contaigability() -> float:
    """A function returning the contaigability"""
    return random.normalvariate(0.4, 0.25)


def rand_int(maximum: int) -> int:
    """A default random integer function"""
    return random.randint(1, maximum)


def nothingness_pdf() -> bool:
    """PDF for nothing happening in a step in the simulation."""
    return bool(random.getrandbits(1))


def death_pdf(_res: float) -> bool:
    """A function that determines whether somebody in recovering state will die."""
    return not one_in_n_prbl(100)


def one_in_n_prbl(samples: int) -> bool:
    """Returns the probability of 1 in n things."""
    return random.randint(1, samples) == 1


def default_initial_state_gen(group_pop: int) -> Tuple[int, List[UnitState]]:
    """A function that randomly returns a unit state."""
    state_list = []
    infected_pop = 0
    for _ in range(group_pop):
        if not one_in_n_prbl(1000):
            state_list.append(UnitState.INTERMEDIATE)
            infected_pop += 1
        else:
            state_list.append(UnitState.HEALTHY)

    if state_list.count(UnitState.INTERMEDIATE) == 0:
        return default_initial_state_gen(group_pop)

    return (infected_pop, state_list)

def group_transfer_pdf() -> bool:
    """This function determines when a group transfer will occur"""
    return True

def group_recieve_pdf(unit: UnitType) -> bool:
    """This function determines the likelihood of a unit joining a group"""
    return True

