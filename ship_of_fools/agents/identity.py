"""TASK-302: identity is NOT assigned at t=0 (doc 3, point 4: "at the start:
identity = undefined"). It emerges from accumulated lived experience, and once
formed it feeds back into behavior with some stickiness — closer to how a
real self-concept works than a simple derived stat would (it doesn't
instantly relabel itself the moment the underlying numbers shift).
"""
from dataclasses import dataclass, field
from typing import Dict, Optional

# how many times a signal must recur before it's strong enough to define an
# identity — a single event should never be enough (doc 3: identity is built,
# not assigned)
FORMATION_THRESHOLD = 5


@dataclass
class Identity:
    label: Optional[str] = None
    counts: Dict[str, int] = field(default_factory=lambda: {
        "leader": 0, "benefactor": 0, "opportunist": 0, "survivor": 0,
    })

    def observe(self, signal: str):
        if signal in self.counts:
            self.counts[signal] += 1

    def resolve(self) -> Optional[str]:
        """Re-evaluate the label from accumulated evidence.

        Some stickiness is intentional: an identity, once formed, does not
        flip the instant a rival count edges ahead by one — it needs to
        clearly dominate (1.3x the count behind the current label) to
        change. This is what lets identity outlast the behavior that
        originally built it (doc 3's "sunk cost" idea)."""
        best_kind, best_count = max(self.counts.items(), key=lambda kv: kv[1])
        if best_count < FORMATION_THRESHOLD:
            return self.label  # not enough evidence yet either way
        if self.label is None:
            self.label = best_kind
        elif best_kind != self.label and best_count > 1.3 * self.counts[self.label]:
            self.label = best_kind
        return self.label
