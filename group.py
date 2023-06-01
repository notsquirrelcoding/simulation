"""A module holding the `Group` class."""
import random
from typing import Callable, List, Tuple, TypedDict, Type
from igraph import Graph, Vertex
from defaults import death_pdf
from unit import UnitType, UnitState
from utils import gen_int_without_repeats


class GroupSummray(TypedDict):
    """
    A summary about a `Group`.
    """
    amount_dead: int
    amount_alive: int
    amount_infected: int
    total_pop: int
    group_id: int
    is_dead: bool
    is_freed: bool


class GroupConfig(TypedDict):
    """
    A doct containing the configuration for a `Group` type.
    """
    pop: int
    id: int
    control_units: list[UnitType]
    control_edges: list[tuple[int, int]]
    infect_pdf: Callable[[UnitType, UnitType], bool]
    resistance_gen: Callable[[], float]
    contaigability_gen: Callable[[], float]
    edge_gen: Callable[[int], int]
    nothing_pdf: Callable[[], bool]
    death_pdf: Callable[[float], bool]
    initial_state_gen: Callable[[int], Tuple[int, List[UnitState]]]
    transfer_pdf: Callable[[], bool]
    recieve_pdf: Callable[[UnitType], bool]
    group_unit_emit_pdf: Callable[[List[UnitType]], UnitType]
    popularity_constant: float
    travel_prob_gen: Callable[[int], List[float]]


class Group:
    """A `Group` class. This class groups `Unit`s together and relates them
    using a graph data structure."""

    def __init__(self, config: GroupConfig) -> None:
        group_pop = config["pop"]
        self._graph = Graph(n=group_pop)

        # Check if group is a control one and check if the
        # amount of units matches the population
        is_control_group = self._is_control_group(config)

        contagability_levels = []
        resistances = []
        states = []
        travel_probs = []
        infected_pop = 0
        # Set the random contagability levels, using the random resistance function
        # assuming that it's not a control group
        if not is_control_group:
            for _ in range(group_pop):
                contagability_levels.append(config["contaigability_gen"]())
                resistances.append(config["resistance_gen"]())
            # Set the states and initial population
            (initial_infected_pop,
             initial_states) = config["initial_state_gen"](group_pop)
            travel_probs = config["travel_prob_gen"](group_pop)
            states = initial_states

            # TODO: Find a way to assign `config["travel_prob_gen"](group_pop)` to `travel_probs` such that it doesn't if it's a control group. In the same way that `states` is initialized.
            # Currently implementing the functionality for group transfers.

            infected_pop = initial_infected_pop


        # Set up config if this is a control gorup
        for unit in config["control_units"]:
            states.append(unit["state"])
            travel_probs.append(unit["travel_prob"])
            if unit["state"] == UnitState.INTERMEDIATE:
                infected_pop += 1
            resistances.append(unit["resistance_level"])
            contagability_levels.append(unit["contagability_level"])

        edges = []

        # Randomly add all the edges if it's not a control group
        if not is_control_group:
            for i in range(group_pop):
                amount_of_neighbors = config["edge_gen"](group_pop)
                for _ in range(amount_of_neighbors):
                    other_vertex_id = gen_int_without_repeats(
                        i, 1, group_pop - 1)
                    edges.append((i, other_vertex_id))

        # Add all the control edges
        for edge in config["control_edges"]:
            edges.append(edge)

        # Get rid of duplicates and add the edges by converting it into a set and back
        connections = list({tuple(sorted(i)) for i in edges})
        self._graph.add_edges(connections)

        # Set the the parameters
        self._infected_pop = infected_pop
        self._dead_pop = 0
        self._total_pop = group_pop
        self._is_wiped = False
        self._is_free = False
        self._group_id = config["id"]
        self._infect_pdf = config["infect_pdf"]
        self._nothing_pdf = config["nothing_pdf"]
        self._edge_gen = config["edge_gen"]
        self._transfer_pdf = config["transfer_pdf"]
        self._emit_pdf = config["group_unit_emit_pdf"]
        self._popularity_constant = config["popularity_constant"]
        self._group_recieve_pdf = config["recieve_pdf"]

        self._graph.vs["contagability_level"] = contagability_levels
        self._graph.vs["resistance_level"] = resistances
        self._graph.vs["state"] = states
        self._graph.vs["travel_prob"] = travel_probs

    def infect_step(self) -> Tuple[bool, bool, bool]:
        """This function is a step in the simulation. All it does is update 
        how many are infected, infect new `Unit`s, etc. It returns a tuple
        of booleans. The first one represents if the group is wiped and
        the second represents if the group is free."""

        group_pop = self._total_pop

        if self._nothing_pdf():
            return (False, False, False)

        self._step_through_intermediate()

        self._loop()

        self._update_graph()

        will_emit = self._transfer_pdf() if group_pop > 0 else False

        # Finally check if all units are dead.
        return (self.is_wiped(), self.is_free(), will_emit)


    def emit_unit(self, unit: UnitType):

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
        self._graph.delete_vertices(chosen_vertex.index)  # type: ignore

    def recieve_unit(self, unit: UnitType):
        """A method that handles recieving a new unit."""
        # x = unit["contagability_level"]
        print(f"a:{unit}")

        edges = []
        new_id = self._graph.vcount()
        self._graph.add_vertices(1)
        amount_of_neighbors = self._edge_gen(self._total_pop - self._dead_pop)
        for _ in range(amount_of_neighbors):
            edges.append((new_id, random.randint(0, self._graph.vcount() - 1)))


        self._graph.vs["contagability_level"].append(
            unit["contagability_level"])
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
            "amount_dead": self._dead_pop,
            "amount_alive": self._total_pop - self._dead_pop,
            "amount_infected": self._infected_pop,
            "total_pop": self._total_pop,
            "group_id": self._group_id,
            "is_freed": self._is_free,
            "is_dead": self._is_wiped
        }

    def is_wiped(self) -> bool:
        """A function that returns a boolean indicating whether the
        group has been wiped out."""
        if self._is_wiped:
            return True
        if self._dead_pop >= self._total_pop:
            self._is_wiped = True
            self._infected_pop = 0
            return True
        return False

    def is_free(self) -> bool:
        """A function that returns a boolean indicating whether the
        group has been freed of the virus. That is, there are no
        more infected units."""
        if self._is_free:
            return True
        if self._infected_pop <= 0 and not self._is_wiped:
            self._is_free = True
            return True
        return False

        # Bug: if two nodes are not connected then they cannot infect each other.

    def _step_through_intermediate(self):
        """A function that steps handles the intermediate units. This function decides whether they
        recover or die."""
        vertex: UnitType
        for vertex in self._graph.vs:  # type: ignore
            if vertex["state"] != UnitState.INTERMEDIATE or self._nothing_pdf():
                continue
            if death_pdf(vertex["resistance_level"]):
                # type: ignore
                self._graph.vs[vertex.index]["state"] = UnitState.DEAD # type: ignore
                self._dead_pop += 1
            else:
                # type: ignore
                self._graph.vs[vertex.index]["state"] = UnitState.HEALTHY # type: ignore
            self._infected_pop -= 1

    def _get_vertices(self, edge) -> Tuple[UnitType, UnitType]:
        """A helper function that gets the vertices given an edge"""
        source_vertex: UnitType = self._graph.vs[edge.source].attributes()
        target_vertex: UnitType = self._graph.vs[edge.target].attributes()
        return (source_vertex, target_vertex)

    def _is_control_group(self, config: GroupConfig) -> bool:
        is_control_group = False

        ctrl_units_len = len(config["control_units"])
        if (ctrl_units_len == config["pop"] and
                ctrl_units_len > 0):
            is_control_group = True
        elif (ctrl_units_len != config["pop"] and
              ctrl_units_len > 0):
            raise TypeError(
                "Number of control units does not match population.")
        if len(config["control_units"]) == 0 and len(config["control_edges"]) > 0:
            raise TypeError(
                "There exist control group edges for nonexistent units.")
        return is_control_group

    def _get_units(self) -> List[UnitType]:
        units = []
        vertex: UnitType
        for vertex in self._graph.vs:  # type: ignore
            units.append(vertex)
        return units

    def _update_graph(self):
        """Deletes the vertices of dead units."""
        dead_units = [
            v.index for v in self._graph.vs if v["state"] == UnitState.DEAD]  # type: ignore
        self._graph.delete_vertices(dead_units)

    def _loop(self):
        """Loops through every connection to progress the simulation."""
        # Loop through all the connections/edges
        for edge in self._graph.es:  # type: ignore
            (source_vertex, target_vertex) = self._get_vertices(edge)

            # The probability that a contaigon will occur.
            will_infect = self._infect_pdf(
                source_vertex, target_vertex)
            if will_infect:
                # Set the infected attribute on the target edge to True.
                self._graph.vs[edge.target]["state"] = UnitState.INTERMEDIATE
                self._infected_pop += 1

    def get_id(self) -> int:
        """Gets the groups ID."""
        return self._group_id

    def get_unit(self) -> UnitType:
        """A function that gets a unit based on the emit PDF."""
        unit = self._emit_pdf(self._get_units())
        print(f"RANDOM UNIT: {unit}")
        return unit

    def get_pop_constant(self) -> float:
        """Gets the popularity constant of this group."""
        return self._popularity_constant

    def acceptance_pdf(self, unit: UnitType) -> bool:
        """A wrapper funtion that determines if a unit will join a group."""
        return self._group_recieve_pdf(unit)


# def get_travel_probs(group_pop: int, is_control_group: bool, gen: Callable[[int], List[int]]) -> List[float]:
#     travel_probs = []
#     if not is_control_group:
#         return gen(group_pop)
    

#     return []
