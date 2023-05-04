from random import randint
from simulation import Simulation
from group import Group, GroupConfig
from unit import UnitType, UnitState
import defaults

if __name__ == "__main__":
    group_options: list[GroupConfig] = []

    control_unit_1 = UnitType({
        "contagability_level": 1.0,
        "resistance_level": 500.0,
        "state": UnitState.HEALTHY,
    })

    control_unit_2 = UnitType({
        "contagability_level": 0.5,
        "resistance_level": 0.5,
        "state": UnitState.HEALTHY,
    })
    
    control_unit_3 = UnitType({
        "contagability_level": 100.0,
        "resistance_level": 100.0,
        "state": UnitState.HEALTHY,
    })

    for i in range(1, 10):

        options: GroupConfig = {
            "group_id": i,
            "group_pop": randint(3, 10),
            "control_units": [],
            "control_edges": [],
            "infect_pdf": defaults.infect_prbl,
            "edge_prbl": defaults.rand_int,
            "resistance_pdf": defaults.resistance,
            "contaigability_pdf": defaults.contaigability,
            "nothing_pdf": defaults.nothingness_pdf,
            "death_pdf": defaults.death_pdf
        }
        group_options.append(options)

    control_group = Group({
        "group_id": 1000,
        "group_pop": 3,
        "control_units": [control_unit_1, control_unit_2, control_unit_3],
        "control_edges": [(0, 1), (1, 2)],
        "infect_pdf": defaults.infect_prbl,
        "edge_prbl": defaults.rand_int,
        "resistance_pdf": defaults.resistance,
        "contaigability_pdf": defaults.contaigability,
        "nothing_pdf": defaults.nothingness_pdf,
        "death_pdf": defaults.death_pdf
    })
    control_group.emit_unit(control_unit_1)
    