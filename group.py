"""A module holding the `Group` class."""
from random import random, randint
import igraph as ig
import itertools

class Group:
    """A `Group` class. This class groups `Unit`s together and relates them.
    """

    def __init__(self, num: int) -> None:
        self._graph = ig.Graph(n=num)
        vulnerabilities = []
        # Set the random vulnerabilities
        for _ in range(num):
            vulnerabilities.append(random())
        self._graph.vs["vulnerability_level"] = vulnerabilities

        edges = []

        # Randomly add all the edges
        for i in range(num):
            for j in range(randint(1, num)):
                edges.append((i, j))

        new_list = []

        for x in itertools.combinations(edges,2):
            new_list.append(x)

        print(self._graph)

    def infect_step(self) -> None:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""
        
        pass
    