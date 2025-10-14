from typing import List
from .models.character import Character
from .models.group import Group
from .models.event import FoodShortageEvent
from .models.enums import GroupIdentity
from .systems.decision_system import DecisionSystem
from .systems.event_system import EventSystem
from .systems.leadership_system import LeadershipSystem

class Simulation:
    def __init__(self, characters: List[Character], groups: List[Group]):
        self.characters = characters
        self.groups = groups
        self.day = 1
        self.decision_system = DecisionSystem()
        self.event_system = EventSystem()
        self.leadership_system = LeadershipSystem(self.characters, self.groups)

        # Subscribe character actions to events
        self.event_system.subscribe("Food Shortage", self.handle_food_shortage)

    def handle_food_shortage(self, character: Character, event: FoodShortageEvent):
        character.needs["hunger"].value -= event.impact["hunger"]
        character.stress += event.impact["stress"]
        print(f"  {character.name} is hungry and stressed due to food shortage.")

    def run_day(self):
        print(f"\n--- Day {self.day} ---")

        # Trigger a random event
        if self.day % 5 == 0:
            event = FoodShortageEvent(self.day)
            print(f"EVENT: {event.description}")
            self.event_system.post(event, self.characters)

        # Characters make decisions
        for char in self.characters:
            decision = self.decision_system.make_decision(char, self.characters)
            print(decision)

        # Update leadership
        self.leadership_system.check_for_leadership_change()

        self.day += 1

    def run_simulation(self, days: int):
        for _ in range(days):
            self.run_day()