"""Personality traits.

These start randomized per agent and drift slowly with lived experience
(see Simulation._update_internal_state) — they are a starting point, not a
fixed label. This is intentional: doc 3, point 1 ("agent's inner world should
really change over time").
"""
import random
from dataclasses import dataclass


@dataclass
class Personality:
    openness: float
    conscientiousness: float
    risk_tolerance: float
    empathy: float
    dominance: float
    conformity: float
    curiosity: float

    @classmethod
    def random(cls, rng: random.Random) -> "Personality":
        def g() -> float:
            # clipped Gaussian around 0.5 — most agents are middling, few are extreme
            return min(1.0, max(0.0, rng.gauss(0.5, 0.18)))

        return cls(
            openness=g(), conscientiousness=g(), risk_tolerance=g(),
            empathy=g(), dominance=g(), conformity=g(), curiosity=g(),
        )
