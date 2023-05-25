from random import randint
from group import GroupConfig
from simulation import Simulation
import defaults

if __name__ == "__main__":
    group_options: list[GroupConfig] = []

    for i in range(1, 20):
        options: GroupConfig = {
            "group_id": i,
            "group_pop": randint(5, 15),
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

    sim = Simulation(group_options, 1000)
    sim.run()
