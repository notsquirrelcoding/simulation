from simulation import Simulation
from group import GroupConfig
from defaults import *
from random import randint

if __name__ == "__main__":
    group_options: list[GroupConfig] = []
    for i in range(1, 20):
        options: GroupConfig = {
            "group_id": i,
            "group_pop": randint(1, 100),
            "control_units": [],
            "control_edges": [],
            "infect_pdf": infect_prbl,
            "edge_prbl": rand_int,
            "random_resistance": normal_random
        }
        group_options.append(options)
    simulation = Simulation(group_options, 100)
    simulation.run()
