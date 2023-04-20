"""A module holding the `Group` class."""
import random
from igraph import Graph

from defaults import prbl
from sim_types import GroupSummray, UnitState, GroupConfig
from unit import Unit


class Group:
    """A `Group` class. This class groups `Unit`s together and relates them
    using a graph data structure."""

    def __init__(self, config: GroupConfig) -> None:
        group_pop = config["group_pop"]

        self._graph = Graph(n=group_pop)

        contagability_levels = []
        # Set the random contagability levels
        for _ in range(group_pop):
            contagability_levels.append(random.random())

        resistances = []
        # Set the random resistances
        for _ in range(group_pop):
            resistances.append(random.random())

        self._graph.vs["contagability_level"] = contagability_levels
        self._graph.vs["resistance_level"] = resistances
        self._graph.vs["state"] = [UnitState.HEALTHY for _ in range(group_pop)]

        edges = []

        # Randomly add all the edges
        for i in range(group_pop):
            for j in range(random.randint(1, group_pop)):
                edges.append((i, j))

        connections = list({tuple(sorted(i)) for i in edges})
        self._graph.add_edges(connections)

        self.amount_dead = 0
        self.total_pop = group_pop
        self._is_wiped = False
        self.group_id = config["group_id"]


    def infect_step(self) -> bool:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""

        # Loop through all the connections/edges
        for edge in self._graph.es: # type: ignore
            if self.amount_dead >= self.total_pop:
                print(f"Group {self.group_id} wiped out.")
                self._is_wiped = True
                return True

            # Get the vertices in each edge
            source_vertex = self._graph.vs[edge.source].attributes()
            target_vertex = self._graph.vs[edge.target].attributes()

            # The probability that a contaigon will occur.
            will_infect = prbl(source_vertex["contagability_level"] /
                (target_vertex["resistance_level"]* 10000))
            if will_infect:
                # Set the infected attribute on the target edge to True.
                self._graph.vs[edge.target]["dead"] = True
                self.amount_dead += 1
        return False
    def __str__(self) -> str:
        string: str = ""
        for vertex in self._graph.vs: # type: ignore
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
            "total_pop": self.total_pop,
            "group_id": self.group_id
        }
    def is_wiped(self) -> bool:
        """A function that returns a boolean indicating whether the
        group has been wiped out."""
        return self._is_wiped
    