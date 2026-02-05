# ==================================================
# FILE 9: social/communication.py
# ==================================================

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import random


class RhetoricTechnique(Enum):
    ETHOS = "ethos"  # Appeal to authority/credibility
    PATHOS = "pathos"  # Appeal to emotion
    LOGOS = "logos"  # Appeal to logic
    KAIROS = "kairos"  # Appeal to timing/urgency
    DEMAGOGY = "demagogy"  # Manipulation of masses


@dataclass
class Message:
    speaker_id: int
    content: str
    technique: RhetoricTechnique
    target_emotion: str
    day: int
    effectiveness: float = 0.0


class Propaganda:
    """Propaganda and manipulation system"""

    @staticmethod
    def craft_message(speaker, technique: RhetoricTechnique,
                      topic: str, target_audience: List) -> Message:
        """Create propaganda message"""

        templates = {
            RhetoricTechnique.ETHOS: [
                f"As your {speaker.role}, I assure you that {topic}",
                f"Trust in my experience - {topic}",
                f"The authorities agree that {topic}"
            ],
            RhetoricTechnique.PATHOS: [
                f"Think of your families! {topic}",
                f"Are you afraid? You should be, because {topic}",
                f"Together we can overcome {topic}"
            ],
            RhetoricTechnique.LOGOS: [
                f"The facts show that {topic}",
                f"Logically speaking, {topic}",
                f"Evidence demonstrates {topic}"
            ],
            RhetoricTechnique.KAIROS: [
                f"We must act NOW! {topic}",
                f"This is our only chance - {topic}",
                f"Time is running out: {topic}"
            ],
            RhetoricTechnique.DEMAGOGY: [
                f"THEY want to {topic}, but WE won't let them!",
                f"The enemy is responsible for {topic}",
                f"Only I can save you from {topic}"
            ]
        }

        content = random.choice(templates[technique])

        # Determine target emotion
        emotion_map = {
            RhetoricTechnique.ETHOS: "trust",
            RhetoricTechnique.PATHOS: random.choice(["fear", "hope", "anger"]),
            RhetoricTechnique.LOGOS: "trust",
            RhetoricTechnique.KAIROS: "fear",
            RhetoricTechnique.DEMAGOGY: "anger"
        }

        return Message(
            speaker_id=speaker.id,
            content=content,
            technique=technique,
            target_emotion=emotion_map[technique],
            day=0
        )

    @staticmethod
    def calculate_effectiveness(message: Message, speaker, audience_member) -> float:
        """How effective is propaganda on this person"""

        base_effectiveness = speaker.speaking_ability / 100

        # Personality factors
        if message.technique == RhetoricTechnique.PATHOS:
            # Emotional people more susceptible
            emotion_factor = audience_member.personality.neuroticism / 100
            base_effectiveness *= (0.7 + emotion_factor * 0.6)

        elif message.technique == RhetoricTechnique.LOGOS:
            # Logical people respond to logic
            logic_factor = audience_member.personality.openness / 100
            base_effectiveness *= (0.7 + logic_factor * 0.6)

        elif message.technique == RhetoricTechnique.DEMAGOGY:
            # Angry, stressed people vulnerable to demagogy
            vulnerability = (audience_member.stress +
                             audience_member.emotional_state.anger) / 200
            base_effectiveness *= (0.5 + vulnerability)

        # Trust in speaker
        trust_factor = audience_member.trust_network.get(speaker.id, 50) / 100
        base_effectiveness *= (0.5 + trust_factor * 0.5)

        # Cognitive bias: confirmation bias
        matches_ideology = (speaker.ideology == audience_member.ideology)
        if matches_ideology:
            base_effectiveness *= 1.5
        else:
            base_effectiveness *= 0.6

        return min(1.0, base_effectiveness)


class EchoChamber:
    """Echo chamber effect - beliefs reinforce within groups"""

    def __init__(self):
        self.chambers: Dict[str, List[int]] = {}  # ideology -> char_ids

    def add_to_chamber(self, char_id: int, ideology: str):
        if ideology not in self.chambers:
            self.chambers[ideology] = []
        if char_id not in self.chambers[ideology]:
            self.chambers[ideology].append(char_id)

    def amplify_beliefs(self, characters: List, ideology: str, amount: float):
        """Beliefs get stronger in echo chamber"""
        if ideology not in self.chambers:
            return

        for char_id in self.chambers[ideology]:
            char = next((c for c in characters if c.id == char_id), None)
            if char:
                # Reinforce beliefs
                for belief in char.belief_system.core_beliefs:
                    char.belief_system.core_beliefs[belief] += amount
                    char.belief_system.core_beliefs[belief] = min(100,
                                                                  char.belief_system.core_beliefs[belief])

                # Reduce doubt
                char.belief_system.doubt_level *= 0.95


class Gaslighting:
    """Authority figures distort reality"""

    @staticmethod
    def distort_memory(target_char, event: str, new_interpretation: str,
                       authority_influence: float) -> bool:
        """Attempt to change someone's memory of an event"""

        # Find memories of this event
        relevant_memories = [m for m in target_char.memories
                             if event.lower() in m.event.lower()]

        if not relevant_memories:
            return False

        # Effectiveness depends on:
        # - Authority influence
        # - Target's stress (confused people easier to gaslight)
        # - Target's doubt level

        susceptibility = (
                (authority_influence / 100) * 0.4 +
                (target_char.stress / 100) * 0.3 +
                (target_char.belief_system.doubt_level / 100) * 0.3
        )

        if random.random() < susceptibility:
            # Memory altered
            for memory in relevant_memories:
                memory.interpretation = new_interpretation

            target_char.belief_system.doubt_level += 15
            return True

        return False

