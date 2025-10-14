from dataclasses import dataclass, field
from typing import Set
from .enums import GroupIdentity

@dataclass
class Event:
    day: int
    type: str
    description: str
    affected_groups: Set[GroupIdentity]
    impact: dict

class FoodShortageEvent(Event):
    def __init__(self, day: int):
        super().__init__(
            day=day,
            type="Food Shortage",
            description="Food supplies are running low.",
            affected_groups={GroupIdentity.WORKERS, GroupIdentity.WOMEN},
            impact={"hunger": 10, "stress": 5}
        )