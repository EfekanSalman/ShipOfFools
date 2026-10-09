"""TASK-205: courts/police — an enforcement institution that only has teeth
once a Leadership institution exists with some legitimacy (doc 1, section 5:
"do not assume institutions exist perfectly from the beginning"). No leader
-> no policing at all, consistent with Leadership's own emergence rule.

Two separate effects, both keyed off legitimacy:
1. REALITY: a thief can get caught and punished, probability scaling with
   the institution's TRUE legitimacy.
2. BELIEF: an agent's own decision to steal is deterred by their PERSONAL
   belief in institutional legitimacy (`Beliefs.institution_trust`), which
   can be wrong in either direction — an agent who (mis)trusts a weak
   institution may be deterred by a threat that barely exists; an agent who
   distrusts a real one won't be deterred even though they'd actually get
   caught. This is the same reality-vs-belief split used everywhere else in
   the project (scarcity, institution_trust itself).
"""
import random


class LawEnforcement:
    def __init__(self, catch_probability_at_full_legitimacy: float = 0.6,
                 punishment_wealth_fraction: float = 0.5):
        self.catch_probability_at_full_legitimacy = catch_probability_at_full_legitimacy
        self.punishment_wealth_fraction = punishment_wealth_fraction

    def catch_probability(self, true_legitimacy: float) -> float:
        return true_legitimacy * self.catch_probability_at_full_legitimacy

    def maybe_catch(self, true_legitimacy: float, rng: random.Random) -> bool:
        return rng.random() < self.catch_probability(true_legitimacy)
