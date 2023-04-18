"""A module holding the `Group` class."""
import random
from igraph import Graph

from defaults import infection_p
from sim_types import GroupSummray


class Group:
    """A `Group` class. This class groups `Unit`s together and relates them."""

    def __init__(self, num: int) -> None:
        self._graph = Graph(n=num)

        contagability_levels = []
        # Set the random contagability levels
        for _ in range(num):
            contagability_levels.append(random.random())

        resistances = []
        # Set the random resistances
        for _ in range(num):
            resistances.append(random.random())

        self._graph.vs["contagability_level"] = contagability_levels
        self._graph.vs["resistance_level"] = resistances
        self._graph.vs["dead"] = [False for _ in range(num)]

        edges = []

        # Randomly add all the edges
        for i in range(num):
            for j in range(random.randint(1, num)):
                edges.append((i, j))

        connections = list({tuple(sorted(i)) for i in edges})
        self._graph.add_edges(connections)

        self.amount_dead = 0
        self.total_pop = num

    def infect_step(self) -> None:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""

        # Loop through all the connections/edges
        for edge in self._graph.es:

            # Get the vertices in each edge
            source_vertex = self._graph.vs[edge.source].attributes()
            target_vertex = self._graph.vs[edge.target].attributes()

            # The probability that a contaigon will occur.
            will_infect = infection_p(source_vertex["contagability_level"] /
                target_vertex["resistance_level"])
            
            if will_infect:
                # Set the infected attribute on the target edge to True.
                self._graph.vs[edge.target]["dead"] = True
                self.amount_dead += 1

    def __str__(self) -> str:
        string: str = ""
        for vertex in self._graph.vs:
            string += str(vertex.attributes())
            string += "\n"

        return string
    def summarize(self) -> GroupSummray:
        """
        A function that returns a summary of the `Group` which
        is contained in the `GroupSummary` type.
        """

        return {
            "amount_dead": self.amount_dead,
            "amount_alive": self.total_pop - self.amount_dead,
            "total_pop": self.total_pop
        }
