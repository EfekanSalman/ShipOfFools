"""The Agent: the core unit of Ship of Fools.

Deliberately NOT a rule-based "smart/stupid" character. Behavior emerges from
the interaction of personality, needs, stress, and (possibly mistaken) beliefs
(see PROJECT_CONSTITUTION.md, rule 1: "no hard-coded good/bad/smart/stupid agents").
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Optional

from .personality import Personality
from .memory import Memory
from .identity import Identity
from ..cognition.beliefs import Beliefs
from ..cognition.mental_models import MentalModel
from ..cognition.metacognition import Metacognition


@dataclass
class NeedState:
    food: float = 0.8
    water: float = 0.8
    social: float = 0.6
    safety: float = 0.7


class Agent:
    def __init__(self, agent_id: int, rng: random.Random):
        self.id = agent_id
        self.rng = rng
        self.personality = Personality.random(rng)
        self.needs = NeedState()
        self.beliefs = Beliefs(
            scarcity_belief=rng.uniform(0.1, 0.4),
            institution_trust=rng.uniform(0.4, 0.8),
        )
        self.memory = Memory()
        self.mental_model = MentalModel()  # TASK-102/103: model of others + reflected self
        self.identity = Identity()         # TASK-302: emerges from lived experience, not assigned
        self.metacognition = Metacognition()  # TASK-601: introspective self-read, can be biased

        # TASK-401/402: lifecycle — founders get an age assigned by Lifecycle
        # at population creation; children start at 0. Identity is NEVER
        # inherited (see population/lifecycle.py docstring) but personality
        # and beliefs partly are.
        self.age_ticks: int = 0
        self.age_years: int = 0
        self.parent_ids = None            # (mother_id, father_id) or None for founders
        self.children = []                # list of Agent refs this agent has parented

        # internal state
        self.stress: float = rng.uniform(0.1, 0.3)
        self.energy: float = 1.0
        self.mood: float = rng.uniform(0.4, 0.7)
        self.health: float = 1.0
        self.wealth: float = 10.0
        self.forage_skill: float = 0.0    # TASK: learning-by-doing — rises each time the agent forages
        self.alive: bool = True
        self.death_cause = None           # "starvation" or "old_age", set when alive flips False
        self.last_action: Optional[str] = None

    @property
    def foolishness(self) -> float:
        """A time-varying STATE, not a fixed trait (doc 2's "Foolishness Index").

        Rises with stress, cognitive rigidity (low openness) and conformity —
        the same agent can be low-foolishness at t=100 and high at t=300.
        """
        rigidity = 1 - self.personality.openness
        return min(1.0, max(0.0,
            0.4 * self.stress + 0.3 * rigidity + 0.3 * self.personality.conformity))

    def is_needy(self) -> bool:
        return self.needs.food < 0.35 or self.needs.water < 0.35
