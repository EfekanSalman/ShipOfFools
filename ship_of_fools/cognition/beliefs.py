"""An agent's subjective model of the world — which can diverge from ground truth.

This is the mechanism behind doc 2, point 3: the ship has one real resource
level, but each agent carries its own (possibly wrong) belief about it.
"""
from dataclasses import dataclass


@dataclass
class Beliefs:
    scarcity_belief: float = 0.3        # 0 = abundance, 1 = severe scarcity, as perceived
    institution_trust: float = 0.6      # 0-1, trust in ship leadership/institutions

    def update_scarcity(self, observed: float, confirmation_bias: float):
        """Blend new evidence into the prior belief.

        confirmation_bias in [0,1] is the weight kept on the *prior* belief —
        higher means the agent discounts new evidence more (confirmation bias).
        """
        self.scarcity_belief = (
            confirmation_bias * self.scarcity_belief + (1 - confirmation_bias) * observed
        )
        self.scarcity_belief = min(1.0, max(0.0, self.scarcity_belief))

    def update_institution_trust(self, observed_legitimacy: float, confirmation_bias: float):
        """Same blending mechanism as scarcity, applied to institutional
        legitimacy (TASK-203). `observed_legitimacy` is a noisy, individually
        perceived read of `Leadership.legitimacy` — not the ground truth
        directly, so an agent's `institution_trust` can end up quite different
        from the institution's real legitimacy (another reality-vs-belief gap,
        same pattern as scarcity)."""
        self.institution_trust = (
            confirmation_bias * self.institution_trust + (1 - confirmation_bias) * observed_legitimacy
        )
        self.institution_trust = min(1.0, max(0.0, self.institution_trust))
