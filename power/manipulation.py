# ==================================================
# FILE 12: power/manipulation.py
# ==================================================

from enum import Enum
from typing import List, Optional
import random


class ManipulationTactic(Enum):
    DIVIDE_AND_CONQUER = "divide_and_conquer"
    FALSE_PROMISES = "false_promises"
    SCAPEGOATING = "scapegoating"
    DISTRACTION = "distraction"
    FEAR_MONGERING = "fear_mongering"
    LOVE_BOMBING = "love_bombing"
    GASLIGHTING = "gaslighting"


class Manipulation:
    """Authority's manipulation toolkit"""

    @staticmethod
    def divide_and_conquer(authority_char, group1: List, group2: List,
                           characters: List) -> bool:
        """Pit two groups against each other"""

        # Create conflict between groups
        issue = random.choice([
            "resource distribution",
            "blame for problems",
            "cultural differences",
            "historical grievances"
        ])

        # Lower trust between groups
        for char1_id in group1:
            char1 = next((c for c in characters if c.id == char1_id), None)
            if char1:
                for char2_id in group2:
                    if char2_id in char1.trust_network:
                        char1.trust_network[char2_id] -= 20

        for char2_id in group2:
            char2 = next((c for c in characters if c.id == char2_id), None)
            if char2:
                for char1_id in group1:
                    if char1_id in char2.trust_network:
                        char2.trust_network[char1_id] -= 20

        return True

    @staticmethod
    def make_false_promises(authority_char, targets: List,
                            promise: str, characters: List) -> float:
        """Promise something with no intention to deliver"""

        belief_rate = 0.0

        for target_id in targets:
            target = next((c for c in characters if c.id == target_id), None)
            if not target:
                continue

            # Naive people believe more
            naivete = target.personality.agreeableness / 100
            trust = target.trust_network.get(authority_char.id, 50) / 100

            belief_chance = naivete * 0.5 + trust * 0.5

            if random.random() < belief_chance:
                # They believe the promise
                target.emotional_state.hope += 20
                target.stress -= 10
                belief_rate += 1
            else:
                # They see through it
                target.trust_network[authority_char.id] = max(0,
                                                              target.trust_network.get(authority_char.id, 50) - 15)
                target.emotional_state.disgust += 15

        return belief_rate / len(targets) if targets else 0

    @staticmethod
    def scapegoat_character(authority_char, scapegoat_id: int,
                            accusation: str, characters: List) -> bool:
        """Blame someone for everything"""

        scapegoat = next((c for c in characters if c.id == scapegoat_id), None)
        if not scapegoat:
            return False

        # Others turn against scapegoat
        for char in characters:
            if char.id == scapegoat_id or char.id == authority_char.id:
                continue

            # Stressed, angry people more likely to accept scapegoat
            susceptibility = (char.stress + char.emotional_state.anger) / 200

            if random.random() < susceptibility:
                char.enemies.add(scapegoat_id)
                char.trust_network[scapegoat_id] = 0
                char.emotional_state.anger -= 10  # Redirect anger

        # Scapegoat suffers
        scapegoat.stress += 30
        scapegoat.emotional_state.fear += 25
        scapegoat.emotional_state.despair += 20

        return True

    @staticmethod
    def distract_with_trivial_issue(authority_char, trivial_issue: str,
                                    characters: List):
        """Focus attention on irrelevant matter"""

        for char in characters:
            if char.id == authority_char.id:
                continue

            # Create memory of trivial issue
            char.add_memory(
                day=0,  # Would be current day
                event=f"Discussion about {trivial_issue}",
                interpretation="This seems important",
                emotional_impact=5,
                witnesses=[c.id for c in characters[:3]]
            )

            # Reduce focus on real problems
            if char.get_critical_needs():
                # They forget about critical needs temporarily
                char.stress -= 5
