# ==================================================
# FILE 15: narrative/story.py
# ==================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict
import random


class StoryArcType(Enum):
    HERO_JOURNEY = "hero_journey"
    TRAGIC_FALL = "tragic_fall"
    REDEMPTION = "redemption"
    CORRUPTION = "corruption"
    SACRIFICE = "sacrifice"
    BETRAYAL = "betrayal"


class StoryBeat(Enum):
    ORDINARY_WORLD = "ordinary_world"
    CALL_TO_ADVENTURE = "call_to_adventure"
    REFUSAL = "refusal"
    MEETING_MENTOR = "meeting_mentor"
    CROSSING_THRESHOLD = "crossing_threshold"
    TESTS_ALLIES_ENEMIES = "tests_allies_enemies"
    APPROACH = "approach"
    ORDEAL = "ordeal"
    REWARD = "reward"
    ROAD_BACK = "road_back"
    RESURRECTION = "resurrection"
    RETURN_WITH_ELIXIR = "return_with_elixir"


@dataclass
class StoryArc:
    """Character's narrative arc"""
    character_id: int
    arc_type: StoryArcType
    current_beat: StoryBeat
    progress: float = 0.0  # 0-100
    key_moments: List[str] = field(default_factory=list)
    transformation: Dict[str, float] = field(default_factory=dict)
    completed: bool = False

    def advance_arc(self, event: str, impact: float):
        """Progress the story arc"""
        self.key_moments.append(event)
        self.progress += impact

        if self.progress >= 100:
            self.completed = True

    def get_next_beat(self) -> Optional[StoryBeat]:
        """What should happen next in this arc"""
        beats = list(StoryBeat)
        current_index = beats.index(self.current_beat)

        if current_index < len(beats) - 1:
            return beats[current_index + 1]
        return None


class NarrativeEngine:
    """Manages character story arcs"""

    def __init__(self):
        self.story_arcs: Dict[int, StoryArc] = {}
        self.plot_threads: List[str] = []
        self.foreshadowing: List[Dict] = []
        self.dramatic_irony: List[Dict] = []

    def assign_arc(self, char_id: int, arc_type: StoryArcType):
        """Assign a narrative arc to character"""
        arc = StoryArc(
            character_id=char_id,
            arc_type=arc_type,
            current_beat=StoryBeat.ORDINARY_WORLD
        )
        self.story_arcs[char_id] = arc

    def auto_assign_arcs(self, characters: List):
        """Automatically assign appropriate arcs"""
        for char in characters:
            if char.role == "steward":
                # The truth-teller
                self.assign_arc(char.id, StoryArcType.TRAGIC_FALL)

            elif char.role == "captain":
                # The authority figure
                self.assign_arc(char.id, StoryArcType.CORRUPTION)

            elif char.role == "officer":
                # The manipulator
                self.assign_arc(char.id, StoryArcType.BETRAYAL)

            elif "professor" in char.name.lower():
                # The intellectual
                self.assign_arc(char.id, StoryArcType.CORRUPTION)

            else:
                # Random arc
                arc_type = random.choice(list(StoryArcType))
                self.assign_arc(char.id, arc_type)

    def add_foreshadowing(self, event: str, future_event: str, day: int):
        """Plant seeds for future events"""
        self.foreshadowing.append({
            'day': day,
            'hint': event,
            'payoff': future_event,
            'revealed': False
        })

    def create_dramatic_irony(self, known_by: List[int],
                              unknown_by: List[int], secret: str):
        """Some characters know something others don't"""
        self.dramatic_irony.append({
            'known_by': known_by,
            'unknown_by': unknown_by,
            'secret': secret,
            'tension': 50.0
        })

    def check_chekovs_gun(self, day: int) -> Optional[Dict]:
        """Check if foreshadowed events should pay off"""
        for item in self.foreshadowing:
            if not item['revealed'] and day - item['day'] > 5:
                if random.random() < 0.3:
                    item['revealed'] = True
                    return item
        return None

