"""Simple episodic memory with a salience-weighted recency window.

Not a full cognitive-science memory model — a computational abstraction
(see PROJECT_CONSTITUTION.md, rule on documenting simplifications).
"""
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryEvent:
    tick: int
    kind: str                       # e.g. "betrayed", "helped", "heard_belief"
    with_agent: Optional[int]
    salience: float                 # 0-1, how emotionally strong the event was


class Memory:
    def __init__(self, capacity: int = 40):
        self.capacity = capacity
        self.events: deque = deque(maxlen=capacity)

    def record(self, tick: int, kind: str, with_agent: Optional[int] = None, salience: float = 0.5):
        self.events.append(MemoryEvent(tick, kind, with_agent, salience))

    def recent_salience_of(self, kind: str, now: int, window: int = 30) -> float:
        """Sum of salience for events of `kind` within the last `window` ticks."""
        return sum(e.salience for e in self.events if e.kind == kind and (now - e.tick) <= window)
