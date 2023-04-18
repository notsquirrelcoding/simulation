from typing import TypedDict

class GroupSummray(TypedDict):
    """
    A summary about a `Group`.
    """
    amount_dead: int
    amount_alive: int
    total_pop: int
    