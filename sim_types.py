from typing import Callable, TypedDict
from enum import Enum

from unit import Unit

class UnitState(Enum):
    """
    An enum representing the states of a unit.
    """
    DEAD = 1
    INTERMEDIATE = 2
    HEALTHY = 3

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
    control_units: list[Unit]
    control_edges: list[tuple[int, int]]
    infect_pdf: Callable[[float], float]
    resist_pdf: Callable[[float], float]
class SimulationConfig(TypedDict):
    """
    A dict containing the options for starting a `Simulation`.
    """

    group_pops: list[int]
    pdf: Callable[[float], float]
    