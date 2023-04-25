from random import randint
from simulation import Simulation
from group import GroupConfig
import defaults

if __name__ == "__main__":
    group_options: list[GroupConfig] = []
    for i in range(1, 20):
        options: GroupConfig = {
            "group_id": i,
            "group_pop": randint(3, 10),
            "control_units": [],
            "control_edges": [],
            "infect_pdf": defaults.infect_prbl,
            "edge_prbl": defaults.rand_int,
            "random_resistance": defaults.normal_random,
            "random_contaigability": defaults.normal_random
        }
        group_options.append(options)
    control_group: GroupConfig = {
            "group_id": 30,
            "group_pop": randint(10, 100),
            "control_units": [],
            "control_edges": [],
            "infect_pdf": defaults.infect_prbl,
            "edge_prbl": defaults.rand_int,
            "random_resistance": defaults.normal_random,
            "random_contaigability": defaults.normal_random 
    }
    group_options.append(control_group)
    simulation = Simulation(group_options, 100)
    simulation.run()
