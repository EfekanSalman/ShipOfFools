from dataclasses import dataclass, field
from typing import List, Dict, Set
from .enums import Ideology, GroupIdentity

@dataclass
class Need:
    name: str
    value: float = 50.0
    critical_threshold: float = 30

    def is_critical(self) -> bool:
        return self.value < self.critical_threshold

from .memory import Memory

@dataclass
class Character:
    id: int
    name: str
    role: str
    groups: Set[GroupIdentity]
    ideology: Ideology
    needs: Dict[str, Need]
    stress: float = 50.0
    trust_in_captain: float = 70.0
    memories: List[Memory] = field(default_factory=list)
    alliances: Set[int] = field(default_factory=set)
    speaking_ability: float = 50.0
    influence: float = 50.0
    is_spokesperson: bool = False

    def add_memory(self, day: int, event: str, interpretation: str,
                   emotional_impact: float, witnesses: List[int], believed_responsible: Set[int]):
        memory = Memory(day, event, interpretation, emotional_impact, witnesses, believed_responsible)
        self.memories.append(memory)
        self.stress += emotional_impact * 0.5
        self.stress = min(100, max(0, self.stress))

    def recall_event(self, event_keyword: str) -> List[Memory]:
        return [m for m in self.memories if event_keyword.lower() in m.event.lower()]

    def update_needs(self, changes: Dict[str, float]):
        for need_name, change in changes.items():
            if need_name in self.needs:
                self.needs[need_name].value += change
                self.needs[need_name].value = min(100, max(0, self.needs[need_name].value))

    def get_critical_needs(self) -> List[str]:
        return [name for name, need in self.needs.items() if need.is_critical()]

    def calculate_satisfaction(self) -> float:
        if not self.needs:
            return 50.0
        return sum(need.value for need in self.needs.values()) / len(self.needs)