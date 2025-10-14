from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class Memory:
    day: int
    event: str
    interpretation: str
    emotional_impact: float
    witnesses: List[int]
    believed_responsible: Set[int] = field(default_factory=set)