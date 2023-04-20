"""A module containing `Simulation` class."""
from pprint import pprint
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
        for _ in range(10):

            group: Group
            for group in self.groups:

                # If the group is not wiped then step through
                if not group.is_wiped():
                    # infect_step() returns true if the group dies out
                    if group.infect_step():
                        self.dead_groups += 1

                # If all groups are dead just return
                if self.dead_groups >= self.num_groups:
                    return
            self.display_data()
            print("==========================================================================")
            self.time += 1
    def display_data(self):
        """Displays the current data"""
        print(f"t={self.time}")
        group: Group
        for group in self.groups:
            pprint(group.summarize())
