# FILE 19: environment/danger.py
# ==================================================
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import random


class DangerType(Enum):
    ICEBERG = "iceberg"
    STORM = "storm"
    EQUIPMENT_FAILURE = "equipment_failure"
    STRUCTURAL_DAMAGE = "structural_damage"
    FIRE = "fire"
    MAN_OVERBOARD = "man_overboard"


@dataclass
class DangerEvent:
    danger_type: DangerType
    severity: float  # 0-100
    day_occurred: int
    resolved: bool = False
    casualties: List[int] = None

    def __post_init__(self):
        if self.casualties is None:
            self.casualties = []


class DangerSystem:
    """Environmental dangers and ship integrity"""

    def __init__(self):
        self.ship_integrity: float = 100.0
        self.active_dangers: List[DangerEvent] = []
        self.danger_history: List[DangerEvent] = []
        self.near_misses: int = 0
        self.catastrophe_imminent: bool = False

    def calculate_danger_level(self, heading: int, temperature: float) -> float:
        """Calculate current danger based on position and conditions"""
        # North (heading 0) is most dangerous
        position_danger = (360 - heading) / 360 * 100

        # Extreme cold is dangerous
        temperature_danger = max(0, (10 - temperature) * 5)

        # Ship integrity affects danger
        integrity_danger = (100 - self.ship_integrity)

        total_danger = (
                position_danger * 0.5 +
                temperature_danger * 0.3 +
                integrity_danger * 0.2
        )

        return min(100, total_danger)

    def check_for_danger_event(self, danger_level: float, day: int) -> Optional[DangerEvent]:
        """Random danger events based on danger level"""
        chance = danger_level / 100 * 0.3  # Up to 30% chance at max danger

        if random.random() < chance:
            danger_type = random.choice(list(DangerType))
            severity = random.uniform(20, min(danger_level, 90))

            event = DangerEvent(
                danger_type=danger_type,
                severity=severity,
                day_occurred=day
            )

            self.active_dangers.append(event)
            self.danger_history.append(event)

            return event

        return None

    def damage_ship(self, amount: float):
        """Ship takes damage"""
        self.ship_integrity -= amount
        self.ship_integrity = max(0, self.ship_integrity)

        if self.ship_integrity < 30:
            self.catastrophe_imminent = True

    def resolve_danger(self, danger: DangerEvent, success: bool):
        """Attempt to resolve a danger"""
        danger.resolved = True

        if not success:
            # Failed to resolve - take damage
            self.damage_ship(danger.severity * 0.5)

        self.active_dangers.remove(danger)

    def check_sinking_conditions(self, danger_level: float) -> bool:
        """Check if ship should sink"""
        if self.ship_integrity <= 0:
            return True

        if danger_level > 95 and random.random() < 0.3:
            return True

        # Multiple active dangers
        if len(self.active_dangers) >= 3 and random.random() < 0.2:
            return True

        return False

