import random
import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from character import Character, PsychologicalState


# An Enum defining event types
class EventType(Enum):
    NATURAL_DISASTER = "Natural Disaster"
    MAN_MADE_EVENT = "Man-Made Event"
    PHILOSOPHICAL_DILEMMA = "Philosophical Dilemma"
    TECHNICAL_FAILURE = "Technical Failure"


class Event:
    """
    A class that represents an event in the simulation.
    """

    def __init__(self, name: str, description: str, event_type: EventType, impact: Dict[str, Any], weight: float = 1.0):
        self.name = name
        self.description = description
        self.event_type = event_type
        self.impact = impact  # A dictionary that defines the impacts of the event on characters.
        self.weight = weight
        self.severity: float = 1.0

    def __str__(self):
        """
        Provides a clean string representation for logging.
        """
        return f"Event: {self.name} ({self.event_type.value}, Severity: {self.severity:.2f})"


class EventSystem:
    """
    The system that manages events within the simulation.
    """

    def __init__(self):
        self.events: List[Event] = self._create_predefined_events()
        logging.info("Event System initialized.")

    def _create_predefined_events(self) -> List[Event]:
        """
        Creates predefined events with assigned weights.
        """
        return [
            Event(
                name="Food Shortage",
                description="Food supplies on the ship are running out faster than expected. Tensions are rising among people.",
                event_type=EventType.NATURAL_DISASTER,
                impact={"hunger_increase": 0.5, "cooperation_decrease": 0.2, "conflict_increase": 0.3},
                weight=3.0  # More likely to occur
            ),
            Event(
                name="Silent Rebellion",
                description="A group of characters secretly begins to sabotage, believing the leadership is not fair.",
                event_type=EventType.MAN_MADE_EVENT,
                impact={"trust_decrease": 0.4, "rebellion_chance_increase": 0.5},
                weight=1.0  # Less likely to occur
            ),
            Event(
                name="Technological Breakdown",
                description="A serious malfunction has occurred in the reactor providing power to the ship. Volunteers are needed for repairs.",
                event_type=EventType.TECHNICAL_FAILURE,
                impact={"stress_increase": 0.3, "cooperation_chance_increase": 0.4},
                weight=2.0  # Moderately likely
            ),
            Event(
                name="Philosophical Dilemma",
                description="Only one more person can board the ship. Should this last person be allowed on board, or should community morals take precedence?",
                event_type=EventType.PHILOSOPHICAL_DILEMMA,
                impact={"moral_distress_increase": 0.6, "cooperation_decrease": 0.1},
                weight=0.5  # Rare event
            )
        ]

    def trigger_random_event(self) -> Optional[Event]:
        """
        Triggers a random event based on a certain chance using weighted selection.
        """
        if random.random() < 0.2:  # trigger event with 20% chance
            weights = [event.weight for event in self.events]
            event = random.choices(self.events, weights=weights, k=1)[0]
            event.severity = random.uniform(0.5, 1.0)  # Set severity at trigger time
            logging.warning(f"=== EVENT TRIGGERED ===\n{event}\nDescription: {event.description}")
            return event
        return None

    def apply_event_impact(self, characters: List[Character], event: Event):
        """
        Applies the impacts of an event on the characters.
        """
        logging.info(f"Applying the impacts of '{event.name}' event...")
        for char in characters:
            changes = {}
            # Apply direct impacts using a dynamic approach and clamp values
            for effect, value in event.impact.items():
                if effect.endswith('_increase'):
                    attr_name = effect.replace('_increase', '')
                    delta = value * event.severity
                    current_value = getattr(char, attr_name)
                    new_value = max(0.0, min(1.0, current_value + delta))
                    setattr(char, attr_name, new_value)
                    changes[attr_name] = delta
                elif effect.endswith('_decrease'):
                    attr_name = effect.replace('_decrease', '')
                    delta = value * event.severity
                    current_value = getattr(char, attr_name)
                    new_value = max(0.0, min(1.0, current_value - delta))
                    setattr(char, attr_name, new_value)
                    changes[attr_name] = -delta

            # Apply impacts based on psychological state
            if char.psychological_state == PsychologicalState.ANXIOUS:
                char.cooperation_chance = max(0.0, min(1.0, char.cooperation_chance - event.impact.get(
                    "cooperation_decrease", 0) * event.severity))
                char.rebellion_chance = max(0.0, min(1.0, char.rebellion_chance + event.impact.get(
                    "rebellion_chance_increase", 0) * event.severity))
            elif char.psychological_state == PsychologicalState.CALM:
                # Calm characters are less affected
                char.cooperation_chance = max(0.0, min(1.0, char.cooperation_chance + event.impact.get(
                    "cooperation_chance_increase", 0) * event.severity * 0.5))
                char.rebellion_chance = max(0.0, min(1.0, char.rebellion_chance - event.impact.get(
                    "rebellion_chance_increase", 0) * event.severity * 0.5))
            elif char.psychological_state == PsychologicalState.DEPRESSED:
                # Depressed characters have a stronger negative reaction
                char.cooperation_chance = max(0.0, min(1.0, char.cooperation_chance - event.impact.get(
                    "cooperation_decrease", 0) * event.severity * 1.5))
                char.rebellion_chance = max(0.0, min(1.0, char.rebellion_chance + event.impact.get(
                    "rebellion_chance_increase", 0) * event.severity * 1.5))
            elif char.psychological_state == PsychologicalState.AGGRESSIVE:
                # Aggressive characters are more likely to rebel
                char.rebellion_chance = max(0.0, min(1.0, char.rebellion_chance + event.impact.get(
                    "rebellion_chance_increase", 0) * event.severity * 2.0))

            logging.info(f"{char.name} is under the event's impact. Total changes: {changes}")
