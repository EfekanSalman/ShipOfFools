"""TASK-601: metacognition — an agent's introspective read of its OWN recent
behavior, distinct from two things that already exist elsewhere:
- `Identity` (agents/identity.py): a slow, categorical label formed from
  LONG-run accumulated evidence (needs 5+ repeats, sticky once formed).
- `MentalModel.reflected_self` (cognition/mental_models.py): a belief about
  how OTHERS see the agent, driven by external feedback (being helped/betrayed).

Metacognition is neither: it's the agent looking at its OWN recent memory and
asking "have I mostly been helping or hurting people lately?" — and, per
doc 2 point 2, this self-read is NOT guaranteed to be accurate. A self-serving
bias (stronger for less open, more stressed agents) can inflate it.
"""
from dataclasses import dataclass


@dataclass
class Metacognition:
    perceived_self_cooperation: float = 0.5  # 0 = "I've mostly been hurting people", 1 = helping

    def introspect(self, agent, tick: int, window: int = 40, bias_strength: float = 0.25):
        """Re-estimate perceived_self_cooperation from the agent's own memory
        of its `gave_help` vs `stole` events, then blend it into the running
        estimate (introspection is not instantaneous or perfectly sharp)."""
        helped = agent.memory.recent_salience_of("gave_help", now=tick, window=window)
        stole = agent.memory.recent_salience_of("stole", now=tick, window=window)
        total = helped + stole
        observed = 0.5 if total <= 0 else helped / total

        # self-serving bias: less open / more stressed agents round their own
        # record up, not down — a mild, directionally realistic distortion
        bias = bias_strength * (1 - agent.personality.openness) * (0.5 if agent.stress > 0.6 else 0.2)
        biased = min(1.0, max(0.0, observed + bias))

        self.perceived_self_cooperation += 0.2 * (biased - self.perceived_self_cooperation)
        return self.perceived_self_cooperation
