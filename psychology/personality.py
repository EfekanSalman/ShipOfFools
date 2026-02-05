# ==================================================
# FILE 2: psychology/personality.py
# ==================================================

from dataclasses import dataclass, field
from typing import Dict
import random


@dataclass
class Personality:
    """Big Five personality model"""
    openness: float = 50.0  # 0-100
    conscientiousness: float = 50.0
    extraversion: float = 50.0
    agreeableness: float = 50.0
    neuroticism: float = 50.0

    def get_trait(self, trait: str) -> float:
        return getattr(self, trait, 50.0)

    def modify_trait(self, trait: str, amount: float):
        current = self.get_trait(trait)
        setattr(self, trait, max(0, min(100, current + amount)))

    def calculate_stress_vulnerability(self) -> float:
        """High neuroticism = more vulnerable to stress"""
        return self.neuroticism / 100

    def calculate_leadership_potential(self) -> float:
        """Leadership based on extraversion and conscientiousness"""
        return (self.extraversion * 0.6 + self.conscientiousness * 0.4) / 100

    def calculate_radicalization_susceptibility(self) -> float:
        """High openness + low agreeableness = more radical"""
        return (self.openness * 0.5 + (100 - self.agreeableness) * 0.5) / 100

    @staticmethod
    def generate_random() -> 'Personality':
        return Personality(
            openness=random.uniform(30, 90),
            conscientiousness=random.uniform(30, 90),
            extraversion=random.uniform(20, 90),
            agreeableness=random.uniform(30, 90),
            neuroticism=random.uniform(20, 80)
        )

