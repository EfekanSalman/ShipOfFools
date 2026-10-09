"""Social cognition: what one agent believes about another (TASK-102), plus a
minimal theory-of-mind layer — what an agent believes others think of *them*
(TASK-103, simplified to one level: "I think people see me as X", not full
recursive "A thinks B thinks C..." — that's a later V-stage).

Perceptions are noisy and personality-biased. Nothing here is guaranteed to
match either the modeled agent's real traits or their real opinion
(doc 2, points 2-3): Reality -> other's real mind -> this agent's model of it
are three different things that can diverge.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class PerceivedOther:
    perceived_trustworthiness: float = 0.5
    perceived_aggression: float = 0.3
    perceived_status: float = 0.5
    # TASK-602 (V6, partial): second-order ToM — "I think THIS SPECIFIC person
    # sees me as roughly this trustworthy", distinct from the population-level
    # `reflected_self` below. Still not full recursive ToM (no "A thinks B
    # thinks C..." chains) — just one extra, per-dyad level.
    they_probably_think_of_me: float = 0.5


class MentalModel:
    """Held by one agent; keyed by the id of each other agent it has modeled."""

    def __init__(self):
        self.of_others: Dict[int, PerceivedOther] = {}
        # theory of mind (simplified): my belief about how others generally see
        # me — a self-projection, not ground truth, and not the same thing as
        # my actual reputation in SocialNetwork.trust.
        self.reflected_self: float = 0.5

    def get(self, other_id: int) -> PerceivedOther:
        if other_id not in self.of_others:
            self.of_others[other_id] = PerceivedOther()
        return self.of_others[other_id]

    def update_from_interaction(self, other_id: int, kind: str, observer_empathy: float):
        """Update the model of `other_id` after an interaction of `kind`.

        Low-empathy observers draw a harsher/noisier inference from the same
        event (doc 3, point 2: the *observer's* traits distort the model)."""
        m = self.get(other_id)
        harshness = 1.0 - 0.4 * observer_empathy
        if kind == "helped":
            m.perceived_trustworthiness = min(1.0, m.perceived_trustworthiness + 0.25)
        elif kind == "betrayed":
            m.perceived_trustworthiness = max(0.0, m.perceived_trustworthiness - 0.35 * harshness)
            m.perceived_aggression = min(1.0, m.perceived_aggression + 0.3 * harshness)
        elif kind == "socialized":
            m.perceived_status = min(1.0, m.perceived_status + 0.05)

    def update_reflected_self(self, feedback: float, rate: float = 0.12):
        """`feedback` in roughly [-0.35, 0.25]: positive when this agent was
        just helped/included, negative when betrayed/exploited. Drifts slowly
        and can end up quite wrong relative to how others actually see this
        agent — that gap is itself a useful metric (see metrics/tracker.py)."""
        target = min(1.0, max(0.0, self.reflected_self + feedback))
        self.reflected_self += rate * (target - self.reflected_self)
        self.reflected_self = min(1.0, max(0.0, self.reflected_self))

    def update_second_order(self, other_id: int, feedback: float, rate: float = 0.15):
        """TASK-602 (V6, partial): same idea as `update_reflected_self`, but
        scoped to ONE specific relationship instead of a population-wide
        impression — "I think THIS person now sees me a bit more/less
        favorably", which can diverge from both reality and from the
        population-level `reflected_self`."""
        m = self.get(other_id)
        target = min(1.0, max(0.0, m.they_probably_think_of_me + feedback))
        m.they_probably_think_of_me += rate * (target - m.they_probably_think_of_me)
        m.they_probably_think_of_me = min(1.0, max(0.0, m.they_probably_think_of_me))
