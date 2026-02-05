# ==================================================
# FILE 18: environment/health.py
# ==================================================

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
import random


class Disease(Enum):
    COMMON_COLD = "common_cold"
    INFLUENZA = "influenza"
    PNEUMONIA = "pneumonia"
    SCURVY = "scurvy"
    HYPOTHERMIA = "hypothermia"
    TYPHUS = "typhus"


@dataclass
class HealthCondition:
    disease: Disease
    severity: float  # 0-100
    contagious: bool
    day_contracted: int
    treated: bool = False

    def progress(self, treatment_quality: float = 0.0):
        """Disease gets worse or better"""
        if self.treated and treatment_quality > 50:
            self.severity -= 5
        else:
            self.severity += random.uniform(2, 8)

        self.severity = max(0, min(100, self.severity))

    def is_fatal(self) -> bool:
        return self.severity > 90


class HealthSystem:
    """Disease and health management"""

    def __init__(self):
        self.sick_characters: Dict[int, List[HealthCondition]] = {}
        self.dead_characters: List[int] = []
        self.outbreak_active: bool = False
        self.epidemic_diseases: List[Disease] = []

    def infect_character(self, char_id: int, disease: Disease,
                         severity: float, day: int):
        """Character contracts disease"""
        condition = HealthCondition(
            disease=disease,
            severity=severity,
            contagious=(disease in [Disease.INFLUENZA, Disease.TYPHUS]),
            day_contracted=day
        )

        if char_id not in self.sick_characters:
            self.sick_characters[char_id] = []

        self.sick_characters[char_id].append(condition)

    def spread_disease(self, characters: List, social_network: Dict,
                       day: int):
        """Contagious diseases spread"""
        new_infections = []

        for char_id, conditions in self.sick_characters.items():
            char = next((c for c in characters if c.id == char_id), None)
            if not char or not char.is_alive:
                continue

            for condition in conditions:
                if not condition.contagious:
                    continue

                # Spread to connected characters
                connections = social_network.get(char_id, set())
                for contact_id in connections:
                    if random.random() < 0.15:  # 15% transmission rate
                        new_infections.append((contact_id, condition.disease))

        # Apply new infections
        for char_id, disease in new_infections:
            self.infect_character(char_id, disease, random.uniform(20, 40), day)

    def daily_health_update(self, characters: List, medicine_available: bool,
                            temperature: float, day: int):
        """Update all health conditions"""
        treatment_quality = 60.0 if medicine_available else 20.0

        for char_id, conditions in list(self.sick_characters.items()):
            char = next((c for c in characters if c.id == char_id), None)
            if not char:
                continue

            for condition in conditions:
                condition.progress(treatment_quality)

                # Cold makes respiratory diseases worse
                if temperature < 5 and condition.disease in [
                    Disease.COMMON_COLD, Disease.PNEUMONIA
                ]:
                    condition.severity += 5

                # Check for death
                if condition.is_fatal():
                    char.is_alive = False
                    self.dead_characters.append(char_id)
                    print(f"    💀 {char.name} died from {condition.disease.value}")
                    return True  # Death occurred

        return False

    def check_outbreak(self) -> bool:
        """Check if we have an outbreak"""
        disease_counts = {}
        for conditions in self.sick_characters.values():
            for condition in conditions:
                disease = condition.disease
                disease_counts[disease] = disease_counts.get(disease, 0) + 1

        for disease, count in disease_counts.items():
            if count >= 3:
                if disease not in self.epidemic_diseases:
                    self.epidemic_diseases.append(disease)
                    self.outbreak_active = True
                    print(f"    🦠 OUTBREAK: {disease.value} epidemic!")
                    return True

        return False