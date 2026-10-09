"""Information transmission: beliefs propagate between agents and can mutate.

This is the mechanism behind rumors / misinformation (doc 1, section 4):
a shared belief has a chance of being distorted in transit, independent of
whether the sender intended to lie.
"""
import random


def transmit_belief(sender, receiver, misinformation_rate: float, confirmation_bias: float,
                     rng: random.Random, tick: int = 0):
    value = sender.beliefs.scarcity_belief
    if rng.random() < misinformation_rate:
        distortion = rng.uniform(0.15, 0.45) * (1 if rng.random() < 0.5 else -1)
        value = min(1.0, max(0.0, value + distortion))
    receiver.beliefs.update_scarcity(value, confirmation_bias)
    receiver.memory.record(tick, "heard_belief", with_agent=sender.id, salience=0.2)
