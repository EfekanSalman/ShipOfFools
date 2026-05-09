# ==================================================
# FILE 7: social/alliance.py
# ==================================================

from dataclasses import dataclass, field
from typing import Set, List, Optional
from enum import Enum
import random


class AllianceType(Enum):
    IDEOLOGICAL = "ideological"  # Shared beliefs
    IDENTITY = "identity"  # Shared group identity
    PRAGMATIC = "pragmatic"  # Mutual benefit
    PROTECTION = "protection"  # Safety in numbers
    REVOLUTIONARY = "revolutionary"  # Overthrow authority


@dataclass
class Alliance:
    members: Set[int]
    alliance_type: AllianceType
    purpose: str
    strength: float = 50.0
    created_day: int = 0
    leader_id: Optional[int] = None
    broken: bool = False
    secrecy_level: float = 0.0  # 0=public, 100=secret conspiracy

    # Alliance dynamics
    internal_trust: float = 70.0
    cohesion: float = 60.0
    radicalization_level: float = 0.0

    def add_member(self, char_id: int):
        self.members.add(char_id)
        self.strength += 5
        # New members lower average trust temporarily
        self.internal_trust *= 0.95

    def remove_member(self, char_id: int):
        self.members.discard(char_id)
        self.strength -= 15
        self.internal_trust -= 10

        if len(self.members) < 2:
            self.broken = True

    def elect_leader(self, characters: List) -> int:
        """Elect most influential member as leader"""
        member_chars = [c for c in characters if c.id in self.members and c.is_alive]
        if not member_chars:
            self.broken = True
            return None

        leader = max(member_chars, key=lambda c: c.influence)
        self.leader_id = leader.id
        return leader.id

    def calculate_power(self, characters: List) -> float:
        """Alliance power = members * average influence * cohesion"""
        member_chars = [c for c in characters if c.id in self.members and c.is_alive]
        if not member_chars:
            return 0.0

        avg_influence = sum(c.influence for c in member_chars) / len(member_chars)
        return len(member_chars) * avg_influence * (self.cohesion / 100)

    def radicalize(self, amount: float):
        """Alliance becomes more radical"""
        self.radicalization_level += amount
        self.radicalization_level = min(100, self.radicalization_level)

        if self.radicalization_level > 70:
            self.alliance_type = AllianceType.REVOLUTIONARY
            self.secrecy_level += 10


class AllianceNetwork:
    """Manages all alliances on the ship"""

    def __init__(self):
        self.alliances: List[Alliance] = []
        self.history: List[str] = []

    def create_alliance(self, members: Set[int], alliance_type: AllianceType,
                        purpose: str, day: int) -> Alliance:
        alliance = Alliance(
            members=members,
            alliance_type=alliance_type,
            purpose=purpose,
            created_day=day
        )
        self.alliances.append(alliance)
        self.history.append(f"Day {day}: Alliance formed - {purpose}")
        return alliance

    def find_alliance(self, char_id: int) -> Optional[Alliance]:
        """Find alliance that character belongs to"""
        for alliance in self.alliances:
            if char_id in alliance.members and not alliance.broken:
                return alliance
        return None

    def merge_alliances(self, alliance1: Alliance, alliance2: Alliance) -> Alliance:
        """Two alliances merge into one"""
        merged = Alliance(
            members=alliance1.members | alliance2.members,
            alliance_type=alliance1.alliance_type,
            purpose=f"Merged: {alliance1.purpose} & {alliance2.purpose}",
            strength=(alliance1.strength + alliance2.strength) / 2
        )

        alliance1.broken = True
        alliance2.broken = True
        self.alliances.append(merged)
        return merged

    def get_active_alliances(self) -> List[Alliance]:
        return [a for a in self.alliances if not a.broken and len(a.members) >= 2]
