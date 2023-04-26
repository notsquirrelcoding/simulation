from random import randint
from simulation import Simulation
from group import GroupConfig
import defaults

if __name__ == "__main__":
    group_options: list[GroupConfig] = []
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
            "nothing_pdf": defaults.nothingness_pdf
        }
        group_options.append(options)

    simulation = Simulation(group_options, 2000)
    simulation.run()
