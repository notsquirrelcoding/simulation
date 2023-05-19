from random import randint
from group import Group, GroupConfig
from simulation import Simulation
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
    control_unit_4 = UnitType({
        "contagability_level": 200.0,
        "resistance_level": -100.0,
        "state": UnitState.DEAD,
    })

    for i in range(1, 5):

        options: GroupConfig = {
            "group_id": i,
            "group_pop": randint(3, 10),
            "control_units": [],
            "control_edges": [],
            "infect_pdf": defaults.infect_pdf,
            "edge_gen": defaults.rand_int,
            "resistance_gen": defaults.resistance,
            "contaigability_gen": defaults.contaigability,
            "nothing_pdf": defaults.nothingness_pdf,
            "death_pdf": defaults.death_pdf,
            "initial_state_gen": defaults.default_initial_state_gen
        }
        group_options.append(options)

    g = Group(group_options[0])

    control_group = Group({
        "group_id": 1000,
        "group_pop": 4,
        "control_units": [control_unit_1, control_unit_2, control_unit_3, control_unit_4],
        "control_edges": [(0, 3), (0, 2), (1, 2)],
        "infect_pdf": defaults.infect_pdf,
        "edge_gen": defaults.rand_int,
        "resistance_gen": defaults.resistance,
        "contaigability_gen": defaults.contaigability,
        "nothing_pdf": defaults.nothingness_pdf,
        "death_pdf": defaults.death_pdf,
        "initial_state_gen": defaults.default_initial_state_gen
    })

    sim = Simulation(group_options, 1000)
    sim.run()
