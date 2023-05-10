from random import randint
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
    control_unit_4 = UnitType({
        "contagability_level": 200.0,
        "resistance_level": -100.0,
        "state": UnitState.DEAD,
    })

    control_group = Group({
        "group_id": 1000,
        "group_pop": 4,
        "control_units": [control_unit_1, control_unit_2, control_unit_3, control_unit_4],
        "control_edges": [(0, 3), (0, 2), (1, 2)],
        "infect_pdf": defaults.infect_pdf,
        "edge_pdf": defaults.rand_int,
        "resistance_pdf": defaults.resistance,
        "contaigability_pdf": defaults.contaigability,
        "nothing_pdf": defaults.nothingness_pdf,
        "death_pdf": defaults.death_pdf
    })

    print("Beginning     =======================")
    print(control_group._graph)
    emitted_unit = control_group.emit_unit(control_unit_2)
    print("Emitted unit. =======================")
    print(control_group._graph)
    control_group.recieve_unit(emitted_unit)
    print("Recieved unit =======================")
    print(control_group._graph)
