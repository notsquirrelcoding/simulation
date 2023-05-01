"""A module containing the `Unit` class."""
from enum import Enum
from typing import TypedDict

class UnitState(Enum):
    """
    An enum representing the states of a unit.
    """
    DEAD = 1
    INTERMEDIATE = 2
    HEALTHY = 3

class UnitType(TypedDict):
    """A type holding all the attributes of a `Unit` type."""
    contagability_level: float
    resistance_level: float
    state: UnitState

class Unit:
    """A unit in the simulation, this is used to place specific units in a group
    that are not random.
    are not random """
    def __init__(self, unit_type: UnitType) -> None:
        """Creates a new instance of a unit. 
        `res` takes in a number in `[0, 1]` which measures the resistance to the plague.
        `con` takes in a number in `[0, 1]` which measures the contaigabiltiy level.
        `state` represents the current state of the person.
        """
        self._res = unit_type['resistance_level']
        self._con = unit_type['contagability_level']
        self._state = unit_type['state']
    