from abc import ABC, abstractmethod
from typing import List
from ..models.character import Character

class DecisionStrategy(ABC):
    @abstractmethod
    def make_decision(self, character: Character, characters: List[Character]):
        pass

class CooperativeStrategy(DecisionStrategy):
    def make_decision(self, character: Character, characters: List[Character]):
        # Simple cooperative decision
        return f"{character.name} decides to cooperate."

class RebelliousStrategy(DecisionStrategy):
    def make_decision(self, character: Character, characters: List[Character]):
        # Simple rebellious decision
        return f"{character.name} decides to rebel."

class DecisionSystem:
    def __init__(self):
        self.strategies = {
            "cooperative": CooperativeStrategy(),
            "rebellious": RebelliousStrategy(),
        }

    def make_decision(self, character: Character, characters: List[Character]):
        # In a more complex simulation, the strategy would be chosen based on the character's state
        strategy = self.strategies["cooperative"]
        if character.stress > 60:
            strategy = self.strategies["rebellious"]

        return strategy.make_decision(character, characters)