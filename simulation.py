"""A module containing `Simulation` class."""
from group import GroupConfig, Group
from unit import UnitType
from utils import return_prob


class Simulation:
    """The `Simulation` class that manages all the groups and
    actually runs the simulation."""

    def __init__(self, group_configs: list[GroupConfig], iterations: int) -> None:
        groups = []
        pop_constant_sum = 0
        for config in group_configs:
            groups.append(Group(config))
            pop_constant_sum += config["popularity_constant"]
            print(pop_constant_sum)

        if abs(1 - pop_constant_sum) > 0.0000000001:
            raise TypeError("Populariry constants do not sum to 1")

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
            print(
                "==========================================================================")
            self.display_data()
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
                    print(
                        "==========================================================================")
                    self.display_data()
                    return
            self._time += 1

    def group_step(self, group: Group):
        """A group step."""

        if group.is_free() or group.is_wiped():
            return

        (is_wiped, is_free, will_transfer) = group.infect_step()
        if is_wiped:
            self._dead_groups += 1
            self._finished_groups += 1
        if is_free:
            self._free_groups += 1
            self._finished_groups += 1

        if will_transfer:
            transferee = group.get_unit()
            destination_group = self._get_group_index(
                self.group_transfer_end_gen(transferee))
            self.group_transfer(
                group, self._groups[destination_group], transferee)

    def group_transfer_end_gen(self, unit: UnitType) -> int:
        """This function determines the ID of the group which the unit will transfer to."""
        while True:
            group: GroupConfig
            for group in self._groups:
                # TODO: Fix this functionaltiy at some point. Make it so that every group is a subset in the set [0,1]. Then choose a random number. Then let the group be the subset that the random number landed in.
                would_join = return_prob(group["popularity_constant"])
                would_accept = group["recieve_pdf"](unit)

                if would_join and would_accept:
                    return group["id"]

    def group_transfer(self, start: Group, end: Group, transferee):
        """A function that transfers a unit between groups"""
        start.emit_unit(transferee)
        end.recieve_unit(transferee)

    def display_data(self):
        """Displays the current data"""
        print(f"t={self._time}")
        group: Group
        for group in self._groups:
            summary = group.summarize()
            (amount_dead, amount_alive,
             amount_infected, total_pop,
             is_freed, is_dead) = (summary["amount_dead"], summary["amount_alive"],
                                   summary["amount_infected"], summary["total_pop"],
                                   summary["is_freed"], summary["is_dead"])
            print(
                f"""Unit {group.get_id()} \t Dead: {amount_dead} \t 
                Alive: {amount_alive} \t Infected: {amount_infected} \t 
                Total: {total_pop} \t Dead: {is_dead} \t Free: {is_freed}""")

    def _get_group_index(self, group_id: int) -> int:
        """Gets a groups index given an ID"""
        group: GroupConfig
        for index, group in enumerate(self._groups):
            if group["id"] == group_id:
                return index
        return -1
