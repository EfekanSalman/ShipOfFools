# ==================================================
# FILE 11: power/hierarchy.py
# ==================================================

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class PowerSource(Enum):
    LEGITIMATE = "legitimate"  # Official position
    COERCIVE = "coercive"  # Force/threat
    REWARD = "reward"  # Can give benefits
    EXPERT = "expert"  # Knowledge/skill
    REFERENT = "referent"  # Charisma/respect
    INFORMATIONAL = "informational"  # Control of information


@dataclass
class PowerStructure:
    """Formal and informal power hierarchies"""

    # Official hierarchy
    official_leader: int
    officers: List[int]
    workers: List[int]

    # Actual power
    actual_power_rankings: Dict[int, float]  # char_id -> power score

    # Shadow government
    shadow_leaders: List[int] = None
    parallel_structure_exists: bool = False

    def calculate_power_score(self, char, characters: List) -> float:
        """Calculate actual power (not just official position)"""
        score = 0.0

        # Official position
        if char.id == self.official_leader:
            score += 40
        elif char.id in self.officers:
            score += 20

        # Influence
        score += char.influence * 0.3

        # Alliance power
        for alliance in [a for a in getattr(char, 'alliances_obj', [])]:
            if hasattr(alliance, 'calculate_power'):
                score += alliance.calculate_power(characters) * 0.2

        # Social network centrality
        # (would need SocialNetwork instance)

        return score

    def identify_power_vacuum(self, characters: List) -> bool:
        """Check if there's a leadership vacuum"""
        leader = next((c for c in characters if c.id == self.official_leader), None)

        if not leader or not leader.is_alive:
            return True

        if leader.influence < 30:
            return True

        # Check if shadow leaders have more power
        if self.shadow_leaders:
            for shadow_id in self.shadow_leaders:
                shadow = next((c for c in characters if c.id == shadow_id), None)
                if shadow and shadow.influence > leader.influence:
                    return True

        return False

    def power_transition(self, old_leader_id: int, new_leader_id: int):
        """Transfer of power"""
        self.official_leader = new_leader_id

        # Remove old leader from officers if they're there
        if old_leader_id in self.officers:
            self.officers.remove(old_leader_id)

    def create_parallel_structure(self, leaders: List[int]):
        """Shadow government emerges"""
        self.shadow_leaders = leaders
        self.parallel_structure_exists = True
