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
        self.free_groups = 0
        self.iterations = iterations
    def run(self):
        """Runs the simulation."""
        for _ in range(0, self.iterations):
            group: Group
            for group in self.groups:
                # If the group is not wiped then step through
                self.group_step(group)
                # If all groups are dead just return
                if self.dead_groups >= self.num_groups:
                    print("All groups have been wiped out.")
                    return
                if self.free_groups >= self.num_groups:
                    print("All groups are free of the virus.")
                    return
            self.display_data()
            print("==========================================================================")
            self.time += 1

    def group_step(self, group: Group):
        """A group step."""
        if group.is_free():
            return

        if not group.is_wiped():
            (is_wiped, is_free) = group.infect_step()
            if is_wiped:
                self.dead_groups += 1
            if is_free:
                self.free_groups += 1

    def group_transfer(self):
        """A function that transfers a unit between groups"""
        pass
    def display_data(self):
        """Displays the current data"""
        print(f"t={self.time}")
        group: Group
        for group in self.groups:
            print(group.summarize())
