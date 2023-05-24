"""A module containing `Simulation` class."""
from group import GroupConfig, Group


class Simulation:
    """The `Simulation` class that manages all the groups and
    actually runs the simulation."""

    def __init__(self, group_configs: list[GroupConfig], iterations: int) -> None:
        groups = []
        for config in group_configs:
            groups.append(Group(config))

        self._groups = groups
        self._num_groups = len(group_configs)
        self._time = 0
        self._dead_groups = 0
        self._free_groups = 0
        self._finished_groups = 0
        self._iterations = iterations

    def run(self):
        """Runs the simulation."""
        for _ in range(0, self._iterations):
            group: Group
            for group in self._groups:
                # If the group is not wiped then step through
                self.group_step(group)
                # If all groups are dead just return
                if self._dead_groups >= self._num_groups:
                    print("All groups have been wiped out.")
                    return
                if self._free_groups >= self._num_groups:
                    print("All groups are free of the virus.")
                    return
                if self._finished_groups >= self._num_groups:
                    print("Simulation completed.")
                    return
            self.display_data()
            print(
                "==========================================================================")
            self._time += 1

    def group_step(self, group: Group):
        """A group step."""
        print(f"Dead groups: {self._dead_groups} \t Freed groups: {self._free_groups} \t Finished groups: {self._finished_groups} \t Total groups: {self._num_groups}")
        if group.is_free() or group.is_wiped():
            return

        (is_wiped, is_free) = group.infect_step()
        if is_wiped:
            print("group dead")
            self._dead_groups += 1
            self._finished_groups += 1
        if is_free:
            print("group free")
            self._free_groups += 1
            self._finished_groups += 1

    def group_transfer(self):
        """A function that transfers a unit between groups"""

    def display_data(self):
        """Displays the current data"""
        print(f"t={self._time}")
        group: Group
        for group in self._groups:
            print(group.summarize())
