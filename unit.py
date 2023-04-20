import igraph as ig

class Unit:
    """A unit in the simulation, this is used to place specific units in a group
    that are not random.
    are not random """
    def __init__(self, vul: float, res: float, infected=False, dead=False) -> None:
        """Creates a new instance of a unit. 
        `vul` takes in a number in `[0, 1]` which measures the vulnerability to the plague.
        `res` takes in a number in `[0, 1]` which measures the resistance to the plague.
        """
        self._vul = vul
        self._res = res
        self._infected = infected
        self._dead = dead
    