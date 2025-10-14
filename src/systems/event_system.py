from typing import List, Dict, Callable
from ..models.event import Event
from ..models.character import Character

class EventSystem:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def post(self, event: Event, characters: List[Character]):
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                for character in characters:
                    if any(g in event.affected_groups for g in character.groups):
                        listener(character, event)