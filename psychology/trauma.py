# ==================================================
# FILE 3: psychology/trauma.py
# ==================================================
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class TraumaType(Enum):
    VIOLENCE = "violence"
    BETRAYAL = "betrayal"
    LOSS = "loss"
    HUMILIATION = "humiliation"
    EXISTENTIAL = "existential"


class TraumaSeverity(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    CRITICAL = 4


@dataclass
class Trauma:
    trauma_type: TraumaType
    severity: TraumaSeverity
    day_occurred: int
    description: str
    triggers: List[str] = field(default_factory=list)
    processed: bool = False
    ptsd_score: float = 0.0

    def age(self, current_day: int) -> int:
        return current_day - self.day_occurred

    def is_fresh(self, current_day: int) -> bool:
        return self.age(current_day) < 7

    def calculate_impact(self, current_day: int) -> float:
        """Trauma impact decreases over time if processed"""
        base_impact = self.severity.value * 10

        if self.processed:
            decay = 0.9 ** self.age(current_day)
            return base_impact * decay
        else:
            # Unprocessed trauma can worsen
            growth = 1.1 ** min(self.age(current_day), 20)
            return base_impact * growth


@dataclass
class PTSDSystem:
    """Post-Traumatic Stress Disorder simulation"""
    traumas: List[Trauma] = field(default_factory=list)
    flashback_triggers: Dict[str, List[Trauma]] = field(default_factory=dict)
    hypervigilance: float = 0.0  # 0-100
    emotional_numbing: float = 0.0  # 0-100

    def add_trauma(self, trauma: Trauma):
        self.traumas.append(trauma)

        # Register triggers
        for trigger in trauma.triggers:
            if trigger not in self.flashback_triggers:
                self.flashback_triggers[trigger] = []
            self.flashback_triggers[trigger].append(trauma)

        # Increase PTSD symptoms
        self.hypervigilance += trauma.severity.value * 5
        if len(self.traumas) > 3:
            self.emotional_numbing += 10

    def check_trigger(self, event_description: str, current_day: int) -> Optional[List[Trauma]]:
        """Check if event triggers flashbacks"""
        triggered = []

        for trigger, traumas in self.flashback_triggers.items():
            if trigger.lower() in event_description.lower():
                for trauma in traumas:
                    if not trauma.processed and trauma.is_fresh(current_day):
                        triggered.append(trauma)

        return triggered if triggered else None

    def calculate_total_impact(self, current_day: int) -> float:
        """Total PTSD impact on character"""
        return sum(t.calculate_impact(current_day) for t in self.traumas)

    def attempt_processing(self, trauma: Trauma, support_level: float) -> bool:
        """Attempt to process trauma with social support"""
        success_chance = support_level / 100

        if random.random() < success_chance:
            trauma.processed = True
            self.hypervigilance = max(0, self.hypervigilance - 10)
            return True
        return False

