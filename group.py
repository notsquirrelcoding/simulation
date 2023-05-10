"""A module holding the `Group` class."""
import random
from typing import Callable, TypedDict, Type
from igraph import Graph, Vertex
from unit import UnitType, UnitState

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
    control_units: list[UnitType]
    control_edges: list[tuple[int, int]]
    infect_pdf: Callable[[UnitType, UnitType], float]
    resistance_pdf: Callable[[], float]
    contaigability_pdf: Callable[[], float]
    edge_pdf: Callable[[int], int]
    nothing_pdf: Callable[[], bool]
    death_pdf: Callable[[float], bool]

class Group:
    """A `Group` class. This class groups `Unit`s together and relates them
    using a graph data structure."""

    def __init__(self, config: GroupConfig) -> None:
        group_pop = config["group_pop"]
        self._graph = Graph(n=group_pop)

        is_control_group = False

        # Check if group is a control one and check if the
        # amount of units matches the population
        ctrl_units_len = len(config["control_units"])
        if (ctrl_units_len == group_pop and
                ctrl_units_len > 0):
            is_control_group = True
        elif (ctrl_units_len != group_pop and
              ctrl_units_len > 0):
            raise TypeError(
                "Number of control units does not match population.")
        if len(config["control_units"]) == 0 and len(config["control_edges"]) > 0:
            raise TypeError(
                "There exist control group edges for nonexistent units.")

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
        # Add the states
        states = []
        if not is_control_group:
            for _ in range(0, group_pop):
                states.append(UnitState.HEALTHY)

        for unit in config["control_units"]:
            states.append(unit["state"])
            resistances.append(unit["resistance_level"])
            contagability_levels.append(unit["contagability_level"])

        edges = []

        # Randomly add all the edges if it's not a control group
        if not is_control_group:
            for i in range(group_pop):
                amount_of_neighbors = config["edge_pdf"](group_pop)
                for _ in range(amount_of_neighbors):
                    edges.append((i, random.randint(1, group_pop - 1)))
        # Add all the control edges
        for edge in config["control_edges"]:
            edges.append(edge)

        # Get rid of duplicates and add the edges by converting it into a set and back
        connections = list({tuple(sorted(i)) for i in edges})
        self._graph.add_edges(connections)

        # Set the the parameters
        self.amount_dead = 0
        self.total_pop = group_pop
        self._is_wiped = False
        self.group_id = config["group_id"]
        self.infect_pdf = config["infect_pdf"]
        self.nothing_pdf = config["nothing_pdf"]
        self.edge_pdf = config["edge_pdf"]

        self._graph.vs["contagability_level"] = contagability_levels
        self._graph.vs["resistance_level"] = resistances
        self._graph.vs["state"] = states

    def infect_step(self) -> bool:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc."""

        # Loop through the recovering
        vertex: UnitType
        for vertex in self._graph.vs:  # type: ignore
            if vertex["state"] == UnitState.HEALTHY:
                continue

        # Loop through all the connections/edges
        for edge in self._graph.es:  # type: ignore
            if self.nothing_pdf():
                continue
            source_vertex: UnitType = self._graph.vs[edge.source].attributes()
            target_vertex: UnitType = self._graph.vs[edge.target].attributes()

            # The probability that a contaigon will occur.
            will_infect = self.infect_pdf(
                source_vertex, target_vertex)
            if will_infect and source_vertex["state"] == UnitState.HEALTHY:
                # Set the infected attribute on the target edge to True.
                self._graph.vs[edge.target]["state"] = UnitState.INTERMEDIATE
                self.amount_dead += 1

            # Finally check if all units are dead.
            if self.amount_dead >= self.total_pop:
                print(f"Group {self.group_id} wiped out.")
                self._is_wiped = True
                return True

        return False

    def emit_unit(self, unit: UnitType) -> UnitType:
        """A group that emits a unit so that it can be transferred to another group"""
        # Get the vertex ID of the unit

        chosen_vertex: Type[Vertex] | None = None

        for vertex in self._graph.vs:  # type: ignore
            # Definetely a better way to do this below by implementing some some sort of python
            # equivilent to Rust's `Into` trait.
            if (
                vertex["state"] == unit["state"]
                and vertex["contagability_level"] == unit["contagability_level"]
                and vertex["resistance_level"] == unit["resistance_level"]
            ):
                chosen_vertex = vertex
                break
        if not chosen_vertex:
            raise TypeError("Vertex not found in group.")
        self._graph.delete_vertices(chosen_vertex.index) # type: ignore
        return unit

    def recieve_unit(self, unit: UnitType):
        """A method that handles recieving a new unit."""
        edges = []
        new_id = self._graph.vcount()
        amount_of_neighbors = self.edge_pdf(self.total_pop - self.amount_dead)
        for _ in range(amount_of_neighbors):
            edges.append((new_id, random.randint(0, self.total_pop - 1)))

        self._graph.add_vertices(1)

        self._graph.vs["contagability_level"].append(unit["contagability_level"])
        self._graph.vs["resistance_level"].append(unit["resistance_level"])
        self._graph.vs["state"].append(unit["state"])
        self._graph.add_edges(edges)

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
