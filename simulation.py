"""A module containing `Simulation` class."""
from group import Group


class Simulation:
    """The `Simulation` class that manages all the groups and
    actually runs the simulation."""
    def __init__(self, num_groups: int, group_pop: int) -> None:
        groups = []
        for i in range(num_groups):
            groups.append(Group(group_pop, group_id=i))
        self.groups = groups
        self.num_groups = num_groups
        self.time = 0
        self.dead_groups = 0
    def run(self):
        """Runs the simulation."""
        for step in range(10000):
            self.time += step
            group: Group
            for group in self.groups:
                if not group.is_wiped():
                    if group.infect_step():
                        self.dead_groups += 1
                if self.dead_groups >= self.num_groups:
                    return
            self.display_data()
            print("==========================================================================")

    def display_data(self):
        """Displays the current data"""
        print(f"t={self.time}")
        group: Group
        for group in self.groups:
            print(group.summarize())

    