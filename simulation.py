"""A module containing `Simulation` class."""
from group import Group


class Simulation:
    """The `Simulation` class that manages all the groups and
    actually runs the simulation."""
    def __init__(self, num_groups: int, group_pop: int) -> None:
        groups = []
        for _ in range(num_groups):
            groups.append(Group(group_pop))
        self.groups = groups
        self.time = 0
    def run(self):
        """Runs the simulation."""

        for t in range(100):
            self.time += t
            group: Group
            for group in self.groups:
                group.infect_step()
                self.display_data()
                print("==========================================================================")
    def display_data(self):
        """Displays the current data"""
        print(f"t={self.time}")
        group: Group
        for group in self.groups:
            print(group.summarize())

    