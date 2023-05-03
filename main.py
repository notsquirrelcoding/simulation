from random import randint
from simulation import Simulation
from group import GroupConfig, Group
from unit import UnitType, UnitState
import defaults

if __name__ == "__main__":
    group_options: list[GroupConfig] = []

    control_unit_1 = UnitType({
        "contagability_level": 1.0,
        "resistance_level": 0.001,
        "state": UnitState.HEALTHY,
    })

    control_unit_2 = UnitType({
        "contagability_level": 0.001,
        "resistance_level": 1.0,
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

    control_group: Group = Group({
        "group_id": 200,
        "group_pop": 2,
        "control_units": [control_unit_1, control_unit_2],
        "control_edges": [(0, 1)],
        "infect_pdf": defaults.infect_prbl,
        "edge_prbl": defaults.rand_int,
        "resistance_pdf": defaults.resistance,
        "contaigability_pdf": defaults.contaigability,
        "nothing_pdf": defaults.nothingness_pdf,
        "death_pdf": defaults.death_pdf
    })

    simulation = Simulation(group_options, 2000)
    simulation.run()
