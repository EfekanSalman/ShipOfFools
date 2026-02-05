# ==================================================
# FILE 13: morality/overton.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class AcceptabilityLevel(Enum):
    UNTHINKABLE = "unthinkable"
    RADICAL = "radical"
    ACCEPTABLE = "acceptable"
    SENSIBLE = "sensible"
    POPULAR = "popular"
    POLICY = "policy"


@dataclass
class OvertonWindow:
    """Overton window - what's socially acceptable shifts over time"""

    behaviors: Dict[str, AcceptabilityLevel] = field(default_factory=dict)
    shift_history: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        # Initialize with default behaviors
        self.behaviors = {
            "violence": AcceptabilityLevel.UNTHINKABLE,
            "theft": AcceptabilityLevel.RADICAL,
            "lying_to_authority": AcceptabilityLevel.RADICAL,
            "hoarding_resources": AcceptabilityLevel.RADICAL,
            "public_protest": AcceptabilityLevel.ACCEPTABLE,
            "questioning_captain": AcceptabilityLevel.SENSIBLE,
            "helping_others": AcceptabilityLevel.POPULAR,
            "following_orders": AcceptabilityLevel.POLICY,
            "scapegoating": AcceptabilityLevel.UNTHINKABLE,
            "torture": AcceptabilityLevel.UNTHINKABLE,
            "cannibalism": AcceptabilityLevel.UNTHINKABLE,
            "mutiny": AcceptabilityLevel.UNTHINKABLE,
            "murder": AcceptabilityLevel.UNTHINKABLE
        }

    def shift_window(self, behavior: str, direction: int, day: int):
        """
        Shift acceptability of a behavior
        direction: +1 = more acceptable, -1 = less acceptable
        """
        if behavior not in self.behaviors:
            return

        current_level = self.behaviors[behavior]
        levels = list(AcceptabilityLevel)
        current_index = levels.index(current_level)

        new_index = max(0, min(len(levels) - 1, current_index + direction))
        new_level = levels[new_index]

        if new_level != current_level:
            self.behaviors[behavior] = new_level
            self.shift_history.append({
                'day': day,
                'behavior': behavior,
                'from': current_level.value,
                'to': new_level.value
            })

            print(f"    📊 OVERTON SHIFT: '{behavior}' is now {new_level.value}")

    def normalize_behavior(self, behavior: str, occurrences: int, day: int):
        """Repeated behavior becomes normalized"""
        # Every 3 occurrences, shift toward acceptable
        if occurrences % 3 == 0:
            self.shift_window(behavior, 1, day)

    def is_acceptable(self, behavior: str) -> bool:
        """Check if behavior is within acceptable range"""
        if behavior not in self.behaviors:
            return False

        level = self.behaviors[behavior]
        return level in [AcceptabilityLevel.ACCEPTABLE,
                         AcceptabilityLevel.SENSIBLE,
                         AcceptabilityLevel.POPULAR,
                         AcceptabilityLevel.POLICY]

    def calculate_shock_value(self, behavior: str) -> float:
        """How shocking is this behavior currently? (0-100)"""
        if behavior not in self.behaviors:
            return 50.0

        shock_map = {
            AcceptabilityLevel.UNTHINKABLE: 100.0,
            AcceptabilityLevel.RADICAL: 70.0,
            AcceptabilityLevel.ACCEPTABLE: 30.0,
            AcceptabilityLevel.SENSIBLE: 15.0,
            AcceptabilityLevel.POPULAR: 5.0,
            AcceptabilityLevel.POLICY: 0.0
        }

        return shock_map[self.behaviors[behavior]]
