# ==================================================
# FILE 10: social/culture.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict, Set
import random


@dataclass
class CulturalNorm:
    """Evolving cultural norms on the ship"""
    name: str
    acceptance: float = 50.0  # 0-100, how accepted is this norm
    emerged_day: int = 0

    def normalize(self, amount: float):
        """Norm becomes more accepted"""
        self.acceptance += amount
        self.acceptance = min(100, self.acceptance)


@dataclass
class Ritual:
    """Group rituals that emerge"""
    name: str
    description: str
    participants: Set[int]
    frequency: str  # "daily", "weekly", "crisis"
    cohesion_bonus: float = 10.0
    created_day: int = 0


class CulturalEvolution:
    """How culture changes on the ship"""

    def __init__(self):
        self.norms: List[CulturalNorm] = []
        self.rituals: List[Ritual] = []
        self.taboo_words: Set[str] = set()
        self.euphemisms: Dict[str, str] = {}  # taboo -> euphemism
        self.jargon: Dict[str, str] = {}  # new word -> meaning
        self.scapegoats: List[int] = []  # character ids who are blamed

        self._init_default_norms()

    def _init_default_norms(self):
        """Initial cultural norms"""
        self.norms = [
            CulturalNorm("respecting_authority", 70.0, 0),
            CulturalNorm("helping_others", 60.0, 0),
            CulturalNorm("non_violence", 80.0, 0),
            CulturalNorm("honesty", 65.0, 0),
            CulturalNorm("equality", 50.0, 0)
        ]

    def introduce_norm(self, name: str, initial_acceptance: float, day: int):
        """New norm emerges"""
        norm = CulturalNorm(name, initial_acceptance, day)
        self.norms.append(norm)
        return norm

    def erode_norm(self, norm_name: str, amount: float):
        """Norm becomes less accepted"""
        for norm in self.norms:
            if norm.name == norm_name:
                norm.acceptance -= amount
                norm.acceptance = max(0, norm.acceptance)

                if norm.acceptance < 30:
                    print(f"    💔 Cultural norm '{norm_name}' has collapsed!")

    def create_ritual(self, name: str, description: str,
                      participants: Set[int], day: int) -> Ritual:
        """Create new ritual"""
        ritual = Ritual(
            name=name,
            description=description,
            participants=participants,
            frequency="weekly",
            created_day=day
        )
        self.rituals.append(ritual)
        return ritual

    def add_taboo_word(self, word: str, euphemism: str):
        """Word becomes taboo"""
        self.taboo_words.add(word.lower())
        self.euphemisms[word.lower()] = euphemism

    def add_jargon(self, word: str, meaning: str):
        """New terminology emerges"""
        self.jargon[word] = meaning

    def designate_scapegoat(self, char_id: int):
        """Someone becomes the scapegoat"""
        if char_id not in self.scapegoats:
            self.scapegoats.append(char_id)

    def calculate_in_group_out_group(self, characters: List) -> Dict[str, List[int]]:
        """Divide characters into in-group and out-group"""
        # Majority ideology is in-group
        ideology_counts = {}
        for char in characters:
            if char.is_alive:
                ideology = char.ideology.value
                ideology_counts[ideology] = ideology_counts.get(ideology, 0) + 1

        if not ideology_counts:
            return {"in_group": [], "out_group": []}

        majority_ideology = max(ideology_counts.items(), key=lambda x: x[1])[0]

        in_group = [c.id for c in characters
                    if c.is_alive and c.ideology.value == majority_ideology]
        out_group = [c.id for c in characters
                     if c.is_alive and c.ideology.value != majority_ideology]

        return {"in_group": in_group, "out_group": out_group}
