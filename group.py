"""A module holding the `Group` class."""
import random
from typing import Callable, TypedDict
from igraph import Graph
from unit import UnitConfig, UnitState

class GroupSummray(TypedDict):
    """
    A summary about a `Group`.
    """
    amount_dead: int
    amount_alive: int
    total_pop: int
    group_id: int


class GroupConfig(TypedDict):
    """
    A doct containing the configuration for a `Group` type.
    """
    group_pop: int
    group_id: int
    control_units: list[UnitConfig]
    control_edges: list[tuple[int, int]]
    infect_pdf: Callable[[float, float], float]
    resistance_pdf: Callable[[], float]
    contaigability_pdf: Callable[[], float]
    edge_prbl: Callable[[int], int]
    nothing_pdf: Callable[[], float]


class Group:
    """A `Group` class. This class groups `Unit`s together and relates them
    using a graph data structure."""

    def __init__(self, config: GroupConfig) -> None:
        group_pop = config["group_pop"]
        self._graph = Graph(n=group_pop)

        is_control_group = False

        # Check if group is a control one and check if the
        # amount of units matches the population
        if len(config["control_units"]) > 0:
            if len(config["control_units"]) != config["group_pop"]:
                print("fpgterfjkpoewqu8rweuirtfewht gertgyhtgr4ehokirfew4")
            is_control_group = True

        contagability_levels = []
        # Set the random contagability levels, using the random resistance function
        # assuming that it's not a control group
        if not is_control_group:
            for _ in range(group_pop):
                contagability_levels.append(config["contaigability_pdf"]())

        resistances = []
        if not is_control_group:
            for _ in range(group_pop):
                resistances.append(config["resistance_pdf"]())

        # Add the control unit levels of contaigability and resistance
        for control_unit in config["control_units"]:
            contagability_levels.append(control_unit["contagability_level"])
            resistances.append(control_unit["resistance_level"])

        states = []
        if not is_control_group:
            for _ in range(0, group_pop):
                states.append(UnitState.HEALTHY)

        for unit in config["control_units"]:
            states.append(unit["state"])

        edges = []

        # Randomly add all the edges
        if not is_control_group:
            for i in range(group_pop):
                amount_of_neighbors = config["edge_prbl"](group_pop)
                for _ in range(amount_of_neighbors):
                    edges.append((i, random.randint(1, group_pop - 1)))
        # Add all the control edges
        for edge in config["control_edges"]:
            edges.append(edge)

        # Get rid of duplicates and add the edges
        connections = list({tuple(sorted(i)) for i in edges})
        self._graph.add_edges(connections)

        # Set the the parametres
        self.amount_dead = 0
        self.total_pop = group_pop
        self._is_wiped = False
        self.group_id = config["group_id"]
        self.infect_pdf = config["infect_pdf"]
        self.nothing_pdf = config["nothing_pdf"]

        # Set the data of the graph
        self._graph.vs["contagability_level"] = contagability_levels
        self._graph.vs["resistance_level"] = resistances
        self._graph.vs["state"] = states

    def infect_step(self) -> bool:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""

        # Loop through all the connections/edges
        for edge in self._graph.es:  # type: ignore

            if self.nothing_pdf() > 0.01:
                continue
            # Get the vertices in each edge
            source_vertex: UnitConfig = self._graph.vs[edge.source].attributes()
            target_vertex: UnitConfig = self._graph.vs[edge.target].attributes()

            # The probability that a contaigon will occur.
            will_infect = self.infect_pdf(
                source_vertex["contagability_level"], target_vertex["resistance_level"])
            if will_infect:
                # Set the infected attribute on the target edge to True.
                self._graph.vs[edge.target]["dead"] = True
                self.amount_dead += 1
            # Finally check if all units are dead.
            if self.amount_dead >= self.total_pop:
                print(f"Group {self.group_id} wiped out.")
                self._is_wiped = True
                return True

        return False

    def __str__(self) -> str:
        string: str = ""
        for vertex in self._graph.vs:  # type: ignore
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
