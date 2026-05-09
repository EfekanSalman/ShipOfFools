# ==================================================
# FILE 14: morality/ethics.py
# ==================================================

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict
import random
from config import Ideology


class EthicalFramework(Enum):
    DEONTOLOGICAL = "deontological"  # Rules-based
    CONSEQUENTIALIST = "consequentialist"  # Ends justify means
    VIRTUE_ETHICS = "virtue_ethics"  # Character-based
    NIHILIST = "nihilist"  # No morality


class MoralDilemmaType(Enum):
    TROLLEY_PROBLEM = "trolley_problem"
    SACRIFICE_ONE_FOR_MANY = "sacrifice_one_for_many"
    THEFT_FOR_SURVIVAL = "theft_for_survival"
    VIOLENCE_FOR_JUSTICE = "violence_for_justice"
    LYING_FOR_GOOD = "lying_for_good"


@dataclass
class MoralDilemma:
    """A moral choice characters must make"""
    dilemma_type: MoralDilemmaType
    description: str
    option_a: str
    option_b: str
    affected_characters: List[int]

    # Consequences
    option_a_consequences: Dict[str, float]
    option_b_consequences: Dict[str, float]


class EthicalSystem:
    """Tracks moral decisions and character alignment"""

    def __init__(self):
        self.moral_scores: Dict[int, float] = {}  # char_id -> morality score
        self.ethical_frameworks: Dict[int, EthicalFramework] = {}
        self.moral_history: List[Dict] = []
        self.collective_guilt: float = 0.0  # 0-100

    def initialize_character(self, char_id: int, ideology: Ideology):
        """Set initial ethical framework based on ideology"""
        framework_map = {
            Ideology.AUTHORITARIAN: EthicalFramework.DEONTOLOGICAL,
            Ideology.REVOLUTIONARY: EthicalFramework.CONSEQUENTIALIST,
            Ideology.CONSERVATIVE: EthicalFramework.VIRTUE_ETHICS,
            Ideology.LIBERAL: EthicalFramework.DEONTOLOGICAL,
            Ideology.ANARCHIST: EthicalFramework.CONSEQUENTIALIST,
            Ideology.NIHILIST: EthicalFramework.NIHILIST
        }

        self.ethical_frameworks[char_id] = framework_map.get(
            ideology, EthicalFramework.VIRTUE_ETHICS
        )
        self.moral_scores[char_id] = 50.0

    def present_dilemma(self, dilemma: MoralDilemma, character) -> str:
        """Character makes moral choice"""
        framework = self.ethical_frameworks.get(character.id,
                                                EthicalFramework.VIRTUE_ETHICS)

        # Decision based on ethical framework
        if framework == EthicalFramework.DEONTOLOGICAL:
            # Rules-based: choose based on principles
            choice = self._deontological_choice(dilemma, character)

        elif framework == EthicalFramework.CONSEQUENTIALIST:
            # Ends justify means: choose best outcome
            choice = self._consequentialist_choice(dilemma, character)

        elif framework == EthicalFramework.VIRTUE_ETHICS:
            # Character-based: what would a virtuous person do?
            choice = self._virtue_choice(dilemma, character)

        else:  # NIHILIST
            # Random or self-serving choice
            choice = random.choice(['option_a', 'option_b'])

        # Record decision
        self.moral_history.append({
            'character_id': character.id,
            'dilemma': dilemma.description,
            'choice': choice,
            'framework': framework.value
        })

        return choice

    def _deontological_choice(self, dilemma: MoralDilemma, character) -> str:
        """Rule-based decision"""
        # Prefers option that doesn't violate core rules
        if "kill" in dilemma.option_a.lower() or "harm" in dilemma.option_a.lower():
            return 'option_b'
        return 'option_a'

    def _consequentialist_choice(self, dilemma: MoralDilemma, character) -> str:
        """Outcome-based decision"""
        # Calculate net benefit of each option
        benefit_a = sum(dilemma.option_a_consequences.values())
        benefit_b = sum(dilemma.option_b_consequences.values())

        return 'option_a' if benefit_a > benefit_b else 'option_b'

    def _virtue_choice(self, dilemma: MoralDilemma, character) -> str:
        """Character-based decision"""
        # What would a person with high agreeableness do?
        if character.personality.agreeableness > 60:
            # Choose option that helps others
            return 'option_b' if "help" in dilemma.option_b.lower() else 'option_a'
        else:
            # Choose self-serving option
            return 'option_a'

    def moral_injury(self, char_id: int, severity: float):
        """Character does something against their values"""
        if char_id in self.moral_scores:
            self.moral_scores[char_id] -= severity
            self.moral_scores[char_id] = max(0, self.moral_scores[char_id])

        self.collective_guilt += severity * 0.1

    def moral_redemption(self, char_id: int, amount: float):
        """Character does something good"""
        if char_id in self.moral_scores:
            self.moral_scores[char_id] += amount
            self.moral_scores[char_id] = min(100, self.moral_scores[char_id])

