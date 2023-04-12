import igraph as ig

class Unit:
    """A unit in the simulation, this can be a person or anything else."""
    def __init__(self, vul: float, res: float) -> None:
        """Creates a new instance of a unit. 
        `vul` takes in a number in `[0, 1]` which measures the vulnerability to the plague.
        `res` takes in a number in `[0, 1]` which measures the resistance to the plague.
        """
        self._vul = vul
        self._res = res
        self._infected = False
        self._dead = False

class Group:
    def __init__(self, population: int) -> None:
        self._graph = ig.Graph(n=population)
    def add_unit(self, unit: Unit) -> None:
        pass
    