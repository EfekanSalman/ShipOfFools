# ==================================================
# FILE 16: narrative/memory.py
# ==================================================

from typing import List, Dict, Optional
import random
from config import CONFIG


class CollectiveMemory:
    """Shared narratives and myths"""

    def __init__(self):
        self.shared_narratives: Dict[str, List[Dict]] = {}  # event -> list of {story,influence,group}
        self.dominant_narrative: Dict[str, str] = {}  # event -> accepted story
        self.belief_adoption: Dict[str, Dict[str, float]] = {}  # event -> group -> adoption rate
        self.dispute_index: Dict[str, float] = {}  # event -> 0-100 polarization
        self.myths: List[Dict] = []
        self.golden_age_myth: Optional[Dict] = None
        self.enemy_narrative: Optional[Dict] = None

    def add_event_narrative(self, event: str, narrator_id: int,
                            narrative: str, influence: float, group: Optional[str] = None):
        """Someone tells their version of an event"""
        if event not in self.shared_narratives:
            self.shared_narratives[event] = []

        self.shared_narratives[event].append({
            'narrator': narrator_id,
            'story': narrative,
            'influence': influence,
            'group': group or 'unknown',
            'believers': []
        })

        # Initialize belief adoption tracking for event
        if event not in self.belief_adoption:
            self.belief_adoption[event] = {}
        if group and group not in self.belief_adoption[event]:
            self.belief_adoption[event][group] = 0.0

        # Update dispute index whenever a new narrative is added
        self._update_dispute_index(event)

    def establish_dominant_narrative(self, event: str):
        """One version becomes "the truth" """
        if event not in self.shared_narratives:
            return

        narratives = self.shared_narratives[event]
        if not narratives:
            return

        # Narrative with most influence wins
        dominant = max(narratives, key=lambda n: n['influence'])
        self.dominant_narrative[event] = dominant['story']

    def _update_dispute_index(self, event: str):
        """Compute polarization for an event based on narrative spread."""
        narratives = self.shared_narratives.get(event, [])
        if not narratives:
            self.dispute_index[event] = 0.0
            return

        # Higher variance in influence across competing groups increases dispute
        by_group: Dict[str, float] = {}
        for n in narratives:
            g = n.get('group', 'unknown')
            by_group[g] = by_group.get(g, 0.0) + n.get('influence', 0.0)

        if len(by_group) <= 1:
            self.dispute_index[event] = 10.0
        else:
            values = list(by_group.values())
            spread = max(values) - min(values)
            self.dispute_index[event] = max(0.0, min(100.0, spread))

    def create_myth(self, myth_name: str, story: str, moral: str):
        """Create a foundational myth"""
        myth = {
            'name': myth_name,
            'story': story,
            'moral': moral,
            'power': 50.0,
            'believers': []
        }
        self.myths.append(myth)
        return myth

    def create_golden_age_myth(self, idealized_past: str):
        """"Things were better before" myth"""
        self.golden_age_myth = {
            'description': idealized_past,
            'power': 30.0,
            'nostalgia_effect': 0.0
        }

    def create_enemy_narrative(self, enemy_group: str, crimes: List[str]):
        """Demonize an out-group"""
        self.enemy_narrative = {
            'enemy': enemy_group,
            'attributed_crimes': crimes,
            'hatred_level': 50.0
        }

    def distort_memory_over_time(self, event: str, days_passed: int):
        """Memories become less accurate over time"""
        if event not in self.shared_narratives:
            return

        # Each week, memories drift
        if not CONFIG.ENABLE_MEMORY_ILLUSIONS:
            return

        if days_passed % 7 == 0:
            for narrative in self.shared_narratives[event]:
                # Distort with probability scaled by drift rate
                if random.random() < (0.2 + CONFIG.MEMORY_DRIFT_RATE * 0.6):
                    narrative['story'] += " [memory distorted]"

                # Small bias: nudge influence toward in-group adoption
                group = narrative.get('group', 'unknown')
                if group != 'unknown':
                    current = self.belief_adoption[event].get(group, 0.0)
                    self.belief_adoption[event][group] = min(100.0, current + 1.0 + CONFIG.MEMORY_DRIFT_RATE * 2)

            # Recompute dispute index after drift
            self._update_dispute_index(event)

