from group import Group


class Simulation:
    def __init__(self, num_groups: int, group_pop: int) -> None:
        groups = []
        for _ in range(num_groups):
            groups.append(Group(group_pop))
        self.groups = groups
        self.time = 0
    def run(self):
        """Runs the simulation."""
        pass

    def display_date(self):
        """Displays the current data"""
        print(f"t={self.time}")
        group: Group
        for group in self.groups:
            print(group.summarize())

        pass
    