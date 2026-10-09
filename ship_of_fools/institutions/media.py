"""TASK-208 (partial — media only; religion/science institutions still not
modeled): a leader institution's belief can reach far more of the population
than organic peer-to-peer rumor spread (information/rumors.py, limited to
local neighbors + a 15% long-range chance). This is a BROADCAST channel
layered ON TOP of the organic one, not a replacement — the same
`transmit_belief` distortion mechanics apply, so state media is not immune
to misinformation, it just has more reach.

No leader -> no broadcast at all (reach scales with TRUE legitimacy, which is
usually small in this model — see KNOWN_ISSUES.md — so this stays a modest
effect in practice, consistent with every other institution here).
"""
import random
from typing import List

from ..information.rumors import transmit_belief


def broadcast(leader, agents: List, true_legitimacy: float, misinformation_rate: float,
              confirmation_bias: float, rng: random.Random, tick: int,
              reach_fraction_at_full_legitimacy: float = 0.5):
    if true_legitimacy <= 0:
        return
    others = [a for a in agents if a.alive and a.id != leader.id]
    reach = int(len(others) * reach_fraction_at_full_legitimacy * true_legitimacy)
    if reach <= 0:
        return
    recipients = rng.sample(others, min(reach, len(others)))
    for recipient in recipients:
        transmit_belief(leader, recipient, misinformation_rate, confirmation_bias, rng, tick=tick)
