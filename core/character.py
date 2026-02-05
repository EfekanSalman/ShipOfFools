# ==================================================
# FILE 6: core/character.py (UPDATED WITH PSYCHOLOGY)
# ==================================================
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import random
from config import CONFIG, Ideology, GroupIdentity
from psychology.personality import Personality
from psychology.emotion import EmotionalState
from psychology.cognition import BeliefSystem, CognitiveBias
from psychology.trauma import PTSDSystem, Trauma, TraumaType, TraumaSeverity


@dataclass
class Need:
    name: str
    value: float  # 0-100
    critical_threshold: float = 30
    importance: float = 1.0  # Weight in decision-making

    def is_critical(self) -> bool:
        return self.value < self.critical_threshold

    def update(self, amount: float):
        self.value = max(0, min(100, self.value + amount))


@dataclass
class Memory:
    day: int
    event: str
    interpretation: str
    emotional_impact: float
    witnesses: List[int]
    emotion_at_time: str = "neutral"
    confidence: float = 50.0
    source_bias: float = 0.0

    def is_traumatic(self) -> bool:
        return abs(self.emotional_impact) > 50


@dataclass
class Character:
    id: int
    name: str
    role: str
    groups: Set[GroupIdentity]
    ideology: Ideology

    # Core stats
    needs: Dict[str, Need]
    stress: float = 50.0
    trust_in_captain: float = 70.0
    influence: float = 50.0
    speaking_ability: float = 50.0

    # Psychology
    personality: Personality = field(default_factory=Personality.generate_random)
    emotional_state: EmotionalState = field(default_factory=EmotionalState)
    belief_system: BeliefSystem = field(default_factory=BeliefSystem)
    ptsd: PTSDSystem = field(default_factory=PTSDSystem)

    # Social
    memories: List[Memory] = field(default_factory=list)
    alliances: Set[int] = field(default_factory=set)
    enemies: Set[int] = field(default_factory=set)
    trust_network: Dict[int, float] = field(default_factory=dict)  # char_id -> trust level

    # Status
    is_alive: bool = True
    is_radicalized: bool = False
    days_without_basic_needs: int = 0

    def add_memory(self, day: int, event: str, interpretation: str,
                   emotional_impact: float, witnesses: List[int]):
        dominant_emotion, _ = self.emotional_state.get_dominant_emotion()

        confidence = 50.0
        source_bias = 0.0

        if CONFIG.ENABLE_MEMORY_ILLUSIONS:
            # Confirmation bias affects confidence
            matches_belief = any(b in interpretation.lower() for b in self.belief_system.core_beliefs.keys())
            confirm_factor = CognitiveBias.confirmation_bias(self, interpretation, matches_belief)
            confidence = max(0.0, min(100.0, 50.0 * confirm_factor))

            # Availability heuristic amplifies recent similar events' impact
            availability = CognitiveBias.availability_heuristic(self, 'fight' if 'fight' in event.lower() else 'event')
            emotional_impact *= availability

            # Anchoring based on first witness truthiness (approx via trust average)
            if witnesses:
                avg_trust = sum(self.trust_network.get(w, 50.0) for w in witnesses) / len(witnesses)
                emotional_impact = CognitiveBias.anchoring_bias(self, emotional_impact, (avg_trust - 50.0) / 10)

            # Personality openness moderates bias intensity
            openness_factor = (100 - self.personality.openness) / 100
            source_bias = CONFIG.MEMORY_BIAS_INTENSITY * openness_factor * 100

        memory = Memory(day, event, interpretation, emotional_impact,
                        witnesses, dominant_emotion, confidence, source_bias)
        self.memories.append(memory)

        # Strong memories cause stress
        self.stress += abs(emotional_impact) * 0.3

        # Check for trauma
        if memory.is_traumatic():
            self._process_traumatic_memory(memory)

    def _process_traumatic_memory(self, memory: Memory):
        """Convert traumatic memory into trauma"""
        trauma_type = self._classify_trauma_type(memory.event)
        severity = self._calculate_trauma_severity(memory.emotional_impact)

        trauma = Trauma(
            trauma_type=trauma_type,
            severity=severity,
            day_occurred=memory.day,
            description=memory.event,
            triggers=[word for word in memory.event.split() if len(word) > 4][:3]
        )

        self.ptsd.add_trauma(trauma)

    def _classify_trauma_type(self, event: str) -> TraumaType:
        event_lower = event.lower()
        if any(word in event_lower for word in ['fight', 'attack', 'violence']):
            return TraumaType.VIOLENCE
        elif any(word in event_lower for word in ['betray', 'lie', 'deceive']):
            return TraumaType.BETRAYAL
        elif any(word in event_lower for word in ['death', 'die', 'lost']):
            return TraumaType.LOSS
        elif any(word in event_lower for word in ['humiliate', 'mock', 'shame']):
            return TraumaType.HUMILIATION
        else:
            return TraumaType.EXISTENTIAL

    def _calculate_trauma_severity(self, emotional_impact: float) -> TraumaSeverity:
        abs_impact = abs(emotional_impact)
        if abs_impact > 75:
            return TraumaSeverity.CRITICAL
        elif abs_impact > 50:
            return TraumaSeverity.SEVERE
        elif abs_impact > 25:
            return TraumaSeverity.MODERATE
        else:
            return TraumaSeverity.MILD

    def update_needs(self, changes: Dict[str, float]):
        for need_name, change in changes.items():
            if need_name in self.needs:
                self.needs[need_name].update(change)

    def get_critical_needs(self) -> List[str]:
        return [name for name, need in self.needs.items() if need.is_critical()]

    def calculate_satisfaction(self) -> float:
        if not self.needs:
            return 50.0

        weighted_sum = sum(need.value * need.importance for need in self.needs.values())
        total_weight = sum(need.importance for need in self.needs.values())

        return weighted_sum / total_weight if total_weight > 0 else 50.0

    def check_radicalization(self, current_day: int):
        """Check if character becomes radicalized"""
        if self.is_radicalized:
            return

        trauma_impact = self.ptsd.calculate_total_impact(current_day)
        unmet_needs = len(self.get_critical_needs())
        betrayal_count = sum(1 for m in self.memories if 'betray' in m.interpretation.lower())

        radicalization_score = (
                (trauma_impact * 0.3) +
                (unmet_needs * 10) +
                (betrayal_count * 15) +
                (self.stress * 0.2) +
                (self.emotional_state.anger * 0.3)
        )

        if radicalization_score > CONFIG.RADICALIZATION_THRESHOLD:
            self._become_radicalized()

    def _become_radicalized(self):
        """Transform into radical"""
        self.is_radicalized = True

        # Ideology shifts
        if self.ideology == Ideology.REFORMIST:
            self.ideology = Ideology.REVOLUTIONARY
        elif self.ideology == Ideology.LIBERAL:
            self.ideology = Ideology.ANARCHIST
        elif self.ideology == Ideology.CONSERVATIVE:
            self.ideology = Ideology.AUTHORITARIAN

        # Psychological changes
        self.emotional_state.anger += 30
        self.emotional_state.trust -= 40
        self.trust_in_captain = max(0, self.trust_in_captain - 50)
        self.belief_system.radicalization_score = 100

        print(f"  🔥 {self.name} has become RADICALIZED! Ideology: {self.ideology.value}")

    def daily_update(self, current_day: int):
        """Daily psychological updates"""
        # Emotions decay
        self.emotional_state.decay_emotions()

        # Check radicalization
        self.check_radicalization(current_day)

        # PTSD effects
        ptsd_impact = self.ptsd.calculate_total_impact(current_day)
        self.stress += ptsd_impact * 0.1

        # Stress slowly decreases if needs are met
        if not self.get_critical_needs():
            self.stress = max(0, self.stress - 2)
        else:
            self.days_without_basic_needs += 1

        # Personality can shift under extreme stress
        if self.stress > 80:
            self.personality.modify_trait('neuroticism', 0.5)
            self.personality.modify_trait('agreeableness', -0.3)
