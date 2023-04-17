"""A module holding the `Group` class."""
import random
from igraph import Graph

from defaults import infection_p


class Group:
    """A `Group` class. This class groups `Unit`s together and relates them."""

    def __init__(self, num: int) -> None:
        self._graph = Graph(n=num)

        vulnerabilities = []
        # Set the random vulnerabilities
        for _ in range(num):
            vulnerabilities.append(random.random())

        resistances = []
        # Set the random resistances
        for _ in range(num):
            resistances.append(random.random())

        self._graph.vs["vulnerability_level"] = vulnerabilities
        self._graph.vs["resistance_level"] = resistances

        edges = []

        # Randomly add all the edges
        for i in range(num):
            for j in range(random.randint(1, num)):
                edges.append((i, j))

        connections = list({tuple(sorted(i)) for i in edges})
        print(connections)
        self._graph.add_edges(connections)

    def infect_step(self) -> None:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""
        for edge in self._graph.es:
            source_vertex = self._graph.vs[edge.source].attributes()
            target_vertex = self._graph.vs[edge.target].attributes()
            will_infect = infection_p(source_vertex["vulnerability_level"] /
                target_vertex["resistance_level"])
            if will_infect:
                # Set the infected attribute on the targte edge to True.
                pass
