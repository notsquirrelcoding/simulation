"""A module containing `Simulation` class."""
from group import GroupConfig, Group

class Simulation:
    """The `Simulation` class that manages all the groups and
    actually runs the simulation."""
    def __init__(self, group_configs: list[GroupConfig], iterations: int) -> None:
        groups = []
        for config in group_configs:
            groups.append(Group(config))

        self.groups = groups
        self.num_groups = len(group_configs)
        self.time = 0
        self.dead_groups = 0
        self.iterations = iterations
    def run(self):
        """Runs the simulation."""
        for _ in range(0, self.iterations):
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
            print(group.summarize())
