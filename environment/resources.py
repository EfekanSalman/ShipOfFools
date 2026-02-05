# ==================================================
# FILE 17: environment/resources.py
# ==================================================

from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class Resource:
    name: str
    quantity: float
    consumption_rate: float
    critical_level: float = 20.0

    def consume(self, amount: float):
        self.quantity -= amount
        self.quantity = max(0, self.quantity)

    def is_critical(self) -> bool:
        return self.quantity < self.critical_level

    def is_depleted(self) -> bool:
        return self.quantity <= 0


class ResourceSystem:
    """Manage ship's resources"""

    def __init__(self):
        self.resources: Dict[str, Resource] = {
            'food': Resource('food', 100.0, 1.5, 20.0),
            'water': Resource('water', 100.0, 2.0, 15.0),
            'fuel': Resource('fuel', 100.0, 0.5, 30.0),
            'blankets': Resource('blankets', 50.0, 0.0, 10.0),
            'medicine': Resource('medicine', 30.0, 0.1, 5.0)
        }

        self.rationing_active: bool = False
        self.black_market_active: bool = False
        self.hoarding_characters: List[int] = []

    def daily_consumption(self, num_characters: int, temperature: float):
        """Daily resource depletion"""
        # Base consumption
        self.resources['food'].consume(num_characters * 0.8)
        self.resources['water'].consume(num_characters * 1.0)
        self.resources['fuel'].consume(0.5)

        # Cold weather increases needs
        if temperature < 5:
            self.resources['blankets'].quantity -= 0.5
            self.resources['fuel'].consume(1.0)

        self.resources['medicine'].consume(0.1)

    def activate_rationing(self):
        """Implement rationing"""
        self.rationing_active = True
        # Reduce consumption rates
        for resource in self.resources.values():
            resource.consumption_rate *= 0.7

    def create_black_market(self):
        """Black market emerges"""
        self.black_market_active = True

    def character_hoards(self, char_id: int, resource_name: str, amount: float):
        """Character secretly hoards resources"""
        if char_id not in self.hoarding_characters:
            self.hoarding_characters.append(char_id)

        if resource_name in self.resources:
            self.resources[resource_name].consume(amount)

    def get_critical_resources(self) -> List[str]:
        """Which resources are running low"""
        return [name for name, res in self.resources.items() if res.is_critical()]

    def resource_crisis(self) -> bool:
        """Are we in a resource crisis?"""
        critical_count = len(self.get_critical_resources())
        return critical_count >= 2

