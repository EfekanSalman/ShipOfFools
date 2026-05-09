# ==================================================
# FILE 20: core/event.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Callable
import random
from config import EventType, GroupIdentity


@dataclass
class Event:
    day: int
    event_type: EventType
    description: str
    affected_groups: Set[GroupIdentity]
    instigator_id: Optional[int] = None
    target_id: Optional[int] = None

    # Effects
    needs_impact: Dict[str, float] = field(default_factory=dict)
    emotion_impact: Dict[str, float] = field(default_factory=dict)
    relationship_impact: Dict[tuple, float] = field(default_factory=dict)

    # Metadata
    severity: float = 50.0
    witnesses: List[int] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)


class EventGenerator:
    """Generates dynamic events based on simulation state"""

    def __init__(self):
        self.event_history: List[Event] = []
        self.event_counts: Dict[EventType, int] = {}
        self.cooldowns: Dict[EventType, int] = {}

    def generate_random_incident(self, characters: List, day: int,
                                 danger_level: float) -> Optional[Event]:
        """Generate random incident"""

        # Higher danger = more incidents
        if random.random() > (danger_level / 200 + 0.1):
            return None

        incident_type = random.choice([
            EventType.THEFT,
            EventType.FIGHT,
            EventType.ABUSE,
            EventType.DEATH  # rare
        ])

        # Check cooldown
        if incident_type in self.cooldowns and self.cooldowns[incident_type] > 0:
            return None

        if incident_type == EventType.THEFT:
            return self._create_theft_event(characters, day)
        elif incident_type == EventType.FIGHT:
            return self._create_fight_event(characters, day)
        elif incident_type == EventType.ABUSE:
            return self._create_abuse_event(characters, day)
        elif incident_type == EventType.DEATH:
            if danger_level > 70 and random.random() < 0.05:
                return self._create_death_event(characters, day)

        return None

    def _create_theft_event(self, characters: List, day: int) -> Event:
        """Someone steals resources"""
        thief = random.choice([c for c in characters if c.is_alive])

        event = Event(
            day=day,
            event_type=EventType.THEFT,
            description=f"{thief.name} was caught stealing food",
            affected_groups={GroupIdentity.WORKERS, GroupIdentity.AUTHORITY},
            instigator_id=thief.id,
            emotion_impact={'trust': -10, 'anger': 15},
            severity=40.0
        )

        self._set_cooldown(EventType.THEFT, 3)
        return event

    def _create_fight_event(self, characters: List, day: int) -> Event:
        """Physical altercation"""
        alive_chars = [c for c in characters if c.is_alive]
        if len(alive_chars) < 2:
            return None

        fighter1 = random.choice(alive_chars)
        fighter2 = random.choice([c for c in alive_chars if c.id != fighter1.id])

        event = Event(
            day=day,
            event_type=EventType.FIGHT,
            description=f"{fighter1.name} and {fighter2.name} fought violently",
            affected_groups=set(fighter1.groups | fighter2.groups),
            instigator_id=fighter1.id,
            target_id=fighter2.id,
            emotion_impact={'fear': 20, 'anger': 25},
            severity=60.0
        )

        self._set_cooldown(EventType.FIGHT, 5)
        return event

    def _create_abuse_event(self, characters: List, day: int) -> Event:
        """Authority abuses power"""
        authority = random.choice([c for c in characters
                                   if GroupIdentity.AUTHORITY in c.groups and c.is_alive])
        victim = random.choice([c for c in characters
                                if GroupIdentity.AUTHORITY not in c.groups and c.is_alive])

        event = Event(
            day=day,
            event_type=EventType.ABUSE,
            description=f"{authority.name} abused {victim.name}",
            affected_groups={GroupIdentity.AUTHORITY, GroupIdentity.WORKERS},
            instigator_id=authority.id,
            target_id=victim.id,
            emotion_impact={'anger': 30, 'fear': 20, 'disgust': 25},
            severity=70.0
        )

        self._set_cooldown(EventType.ABUSE, 7)
        return event

    def _create_death_event(self, characters: List, day: int) -> Event:
        """Someone dies (accident or natural causes)"""
        victim = random.choice([c for c in characters if c.is_alive])
        victim.is_alive = False

        event = Event(
            day=day,
            event_type=EventType.DEATH,
            description=f"{victim.name} died in an accident",
            affected_groups=victim.groups,
            target_id=victim.id,
            emotion_impact={'fear': 40, 'despair': 35, 'trust': -20},
            severity=100.0
        )

        return event

    def _set_cooldown(self, event_type: EventType, days: int):
        """Prevent event from happening again too soon"""
        self.cooldowns[event_type] = days

    def decrement_cooldowns(self):
        """Reduce cooldowns each day"""
        for event_type in list(self.cooldowns.keys()):
            self.cooldowns[event_type] -= 1
            if self.cooldowns[event_type] <= 0:
                del self.cooldowns[event_type]

    def record_event(self, event: Event):
        """Record event in history"""
        self.event_history.append(event)
        self.event_counts[event.event_type] = self.event_counts.get(event.event_type, 0) + 1

