import igraph as ig
from sim_types import UnitState

class Unit:
    """A unit in the simulation, this is used to place specific units in a group
    that are not random.
    are not random """
    def __init__(self, vul: float, state: UnitState) -> None:
        """Creates a new instance of a unit. 
        `vul` takes in a number in `[0, 1]` which measures the vulnerability to the plague.
        `state` represents the current state of the person.
        """
        self._vul = vul
        self._state = state
    