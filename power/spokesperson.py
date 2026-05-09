# ==================================================
# FILE: power/spokesperson.py
# ==================================================
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum

from config import GroupIdentity


class NegotiationStyle(Enum):
    CONCILIATORY = "conciliatory"
    PRAGMATIC = "pragmatic"
    CONFRONTATIONAL = "confrontational"


@dataclass
class Spokesperson:
    char_id: int
    group: GroupIdentity
    mandate: float = 50.0  # 0-100, perceived legitimacy by group members
    radicalization: float = 0.0  # 0-100
    negotiation_style: NegotiationStyle = NegotiationStyle.PRAGMATIC

    def adjust_mandate(self, amount: float):
        self.mandate = max(0.0, min(100.0, self.mandate + amount))

    def adjust_radicalization(self, amount: float):
        self.radicalization = max(0.0, min(100.0, self.radicalization + amount))


class SpokespersonRegistry:
    """Tracks spokespersons for each identity group."""

    def __init__(self):
        self.by_group: Dict[GroupIdentity, Spokesperson] = {}

    def set_spokesperson(self, group: GroupIdentity, char_id: int,
                         mandate: float = 50.0,
                         style: NegotiationStyle = NegotiationStyle.PRAGMATIC):
        self.by_group[group] = Spokesperson(
            char_id=char_id,
            group=group,
            mandate=mandate,
            negotiation_style=style,
        )

    def get(self, group: GroupIdentity) -> Optional[Spokesperson]:
        return self.by_group.get(group)

    def remove(self, group: GroupIdentity):
        if group in self.by_group:
            del self.by_group[group]

    def all(self) -> List[Spokesperson]:
        return list(self.by_group.values())
