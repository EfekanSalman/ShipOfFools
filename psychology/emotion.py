# ==================================================
# FILE 4: psychology/emotion.py
# ==================================================

from dataclasses import dataclass, field
from typing import Dict, List, Set
import random

from config import CONFIG


@dataclass
class EmotionalState:
    """Character's current emotional state"""
    fear: float = 0.0  # 0-100
    anger: float = 0.0
    hope: float = 50.0
    despair: float = 0.0
    trust: float = 50.0
    disgust: float = 0.0

    def get_dominant_emotion(self) -> tuple[str, float]:
        """Returns (emotion_name, intensity)"""
        emotions = {
            'fear': self.fear,
            'anger': self.anger,
            'hope': self.hope,
            'despair': self.despair,
            'trust': self.trust,
            'disgust': self.disgust
        }
        dominant = max(emotions.items(), key=lambda x: x[1])
        return dominant

    def modify_emotion(self, emotion: str, amount: float):
        if hasattr(self, emotion):
            current = getattr(self, emotion)
            setattr(self, emotion, max(0, min(100, current + amount)))

    def decay_emotions(self, rate: float = 0.05):
        """Emotions naturally decay over time"""
        self.fear *= (1 - rate)
        self.anger *= (1 - rate)
        self.despair *= (1 - rate)
        self.disgust *= (1 - rate)

        # Hope and trust decay slower
        self.hope = max(10, self.hope * (1 - rate / 2))
        self.trust = max(10, self.trust * (1 - rate / 2))


class EmotionalContagion:
    """Emotions spread through social network"""

    @staticmethod
    def spread_emotion(source_char, target_char, emotion: str,
                       intensity: float, relationship_strength: float) -> float:
        """
        Emotions spread based on:
        - Intensity of source emotion
        - Relationship strength
        - Target's personality (neuroticism)
        """
        base_spread = intensity * relationship_strength * CONFIG.EMOTION_CONTAGION_RATE

        # Neurotic people catch emotions more easily
        susceptibility = target_char.personality.neuroticism / 100

        spread_amount = base_spread * (0.5 + susceptibility * 0.5)

        return spread_amount

    @staticmethod
    def mob_mentality(characters: List, emotion: str, threshold: float = 60.0) -> bool:
        """Check if mob mentality is triggered"""
        high_emotion_count = sum(
            1 for char in characters
            if getattr(char.emotional_state, emotion, 0) > threshold
        )

        ratio = high_emotion_count / len(characters)
        return ratio > 0.4  # 40% threshold for mob

