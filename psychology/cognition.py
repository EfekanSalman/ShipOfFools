# ==================================================
# FILE 5: psychology/cognition.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict
import random


class CognitiveBias:
    """Various cognitive biases that affect decision-making"""

    @staticmethod
    def confirmation_bias(character, new_info: str, matches_belief: bool) -> float:
        """People accept info that matches beliefs, reject contradictory"""
        if matches_belief:
            return 1.5  # Amplify confirming evidence
        else:
            # High openness = less bias
            openness = character.personality.openness / 100
            return 0.3 + (openness * 0.5)  # Reduce contradictory evidence

    @staticmethod
    def availability_heuristic(character, event_type: str) -> float:
        """Recent/dramatic events seem more likely"""
        recent_memories = [m for m in character.memories[-5:]
                           if event_type.lower() in m.event.lower()]

        if recent_memories:
            return 1.0 + (len(recent_memories) * 0.3)
        return 1.0

    @staticmethod
    def anchoring_bias(character, initial_value: float, adjustment: float) -> float:
        """First impression anchors later judgments"""
        # Low conscientiousness = more susceptible to anchoring
        susceptibility = (100 - character.personality.conscientiousness) / 100

        return initial_value + (adjustment * (0.3 + susceptibility * 0.4))

    @staticmethod
    def groupthink(alliance_members: List, dissenting_opinion: bool) -> bool:
        """Group pressure suppresses dissent"""
        if not dissenting_opinion:
            return True

        # Larger groups = more groupthink
        pressure = min(len(alliance_members) / 10, 0.9)

        return random.random() > pressure

    @staticmethod
    def sunk_cost_fallacy(character, days_invested: int) -> float:
        """More invested = harder to change course"""
        return 1.0 + (days_invested * 0.05)


@dataclass
class BeliefSystem:
    """Character's beliefs and how they change"""
    core_beliefs: Dict[str, float] = field(default_factory=dict)  # belief -> strength (0-100)
    doubt_level: float = 0.0  # 0-100
    radicalization_score: float = 0.0  # 0-100

    def add_belief(self, belief: str, strength: float = 50.0):
        self.core_beliefs[belief] = strength

    def challenge_belief(self, belief: str, evidence_strength: float,
                         character_openness: float) -> bool:
        """Attempt to change a belief"""
        if belief not in self.core_beliefs:
            return False

        current_strength = self.core_beliefs[belief]

        # Openness makes beliefs more flexible
        flexibility = character_openness / 100

        change_threshold = current_strength * (1 - flexibility * 0.5)

        if evidence_strength > change_threshold:
            # Belief shaken
            self.core_beliefs[belief] *= 0.7
            self.doubt_level += 10
            return True
        else:
            # Belief reinforced (backfire effect)
            self.core_beliefs[belief] = min(100, current_strength * 1.1)
            return False

    def radicalize(self, trauma_score: float, group_pressure: float):
        """Trauma + group pressure = radicalization"""
        radicalization_force = (trauma_score + group_pressure) / 2

        self.radicalization_score += radicalization_force * 0.1
        self.radicalization_score = min(100, self.radicalization_score)

        # Radicalization reduces doubt
        self.doubt_level *= 0.9

