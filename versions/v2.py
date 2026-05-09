
# FILE 19: environment/danger.py
# ==================================================
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import random


class DangerType(Enum):
    ICEBERG = "iceberg"
    STORM = "storm"
    EQUIPMENT_FAILURE = "equipment_failure"
    STRUCTURAL_DAMAGE = "structural_damage"
    FIRE = "fire"
    MAN_OVERBOARD = "man_overboard"


@dataclass
class DangerEvent:
    danger_type: DangerType
    severity: float  # 0-100
    day_occurred: int
    resolved: bool = False
    casualties: List[int] = None

    def __post_init__(self):
        if self.casualties is None:
            self.casualties = []


class DangerSystem:
    """Environmental dangers and ship integrity"""

    def __init__(self):
        self.ship_integrity: float = 100.0
        self.active_dangers: List[DangerEvent] = []
        self.danger_history: List[DangerEvent] = []
        self.near_misses: int = 0
        self.catastrophe_imminent: bool = False

    def calculate_danger_level(self, heading: int, temperature: float) -> float:
        """Calculate current danger based on position and conditions"""
        # North (heading 0) is most dangerous
        position_danger = (360 - heading) / 360 * 100

        # Extreme cold is dangerous
        temperature_danger = max(0, (10 - temperature) * 5)

        # Ship integrity affects danger
        integrity_danger = (100 - self.ship_integrity)

        total_danger = (
                position_danger * 0.5 +
                temperature_danger * 0.3 +
                integrity_danger * 0.2
        )

        return min(100, total_danger)

    def check_for_danger_event(self, danger_level: float, day: int) -> Optional[DangerEvent]:
        """Random danger events based on danger level"""
        chance = danger_level / 100 * 0.3  # Up to 30% chance at max danger

        if random.random() < chance:
            danger_type = random.choice(list(DangerType))
            severity = random.uniform(20, min(danger_level, 90))

            event = DangerEvent(
                danger_type=danger_type,
                severity=severity,
                day_occurred=day
            )

            self.active_dangers.append(event)
            self.danger_history.append(event)

            return event

        return None

    def damage_ship(self, amount: float):
        """Ship takes damage"""
        self.ship_integrity -= amount
        self.ship_integrity = max(0, self.ship_integrity)

        if self.ship_integrity < 30:
            self.catastrophe_imminent = True

    def resolve_danger(self, danger: DangerEvent, success: bool):
        """Attempt to resolve a danger"""
        danger.resolved = True

        if not success:
            # Failed to resolve - take damage
            self.damage_ship(danger.severity * 0.5)

        self.active_dangers.remove(danger)

    def check_sinking_conditions(self, danger_level: float) -> bool:
        """Check if ship should sink"""
        if self.ship_integrity <= 0:
            return True

        if danger_level > 95 and random.random() < 0.3:
            return True

        # Multiple active dangers
        if len(self.active_dangers) >= 3 and random.random() < 0.2:
            return True

        return False


# ==================================================
# FILE 20: core/event.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Callable
import random


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


# ==================================================
# FILE 21: core/ship.py (MAIN INTEGRATION)
# ==================================================

class Ship:
    """Main ship class integrating all systems"""

    def __init__(self):
        # Core state
        self.day = 1
        self.heading = 0  # 0=North (danger), 180=South (safety)
        self.temperature = CONFIG.STARTING_TEMPERATURE

        # Characters
        self.characters: List[Character] = []

        # Systems
        self.danger_system = DangerSystem()
        self.resource_system = ResourceSystem()
        self.health_system = HealthSystem()
        self.alliance_network = AllianceNetwork()
        self.event_generator = EventGenerator()
        self.overton_window = OvertonWindow()
        self.ethical_system = EthicalSystem()
        self.narrative_engine = NarrativeEngine()
        self.collective_memory = CollectiveMemory()
        self.cultural_evolution = CulturalEvolution()
        self.power_structure: Optional[PowerStructure] = None

        # Simulation state
        self.captain_authority = 100.0
        self.social_cohesion = 70.0
        self.philosophical_tension = 30.0
        self.simulation_active = True

        # Statistics
        self.protests_held = 0
        self.mutinies_attempted = 0
        self.concessions_granted = 0

    def initialize(self):
        """Setup initial state"""
        self._create_default_characters()
        self._setup_power_structure()
        self._initialize_character_systems()
        self.narrative_engine.auto_assign_arcs(self.characters)
        self._create_golden_age_myth()

    def _create_default_characters(self):
        """Create all characters"""
        char_templates = [
            {
                'id': 1, 'name': 'Captain', 'role': 'captain',
                'groups': {GroupIdentity.AUTHORITY},
                'ideology': Ideology.AUTHORITARIAN,
                'needs': {'power': Need('power', 90), 'respect': Need('respect', 80)},
                'influence': 90, 'speaking_ability': 80
            },
            {
                'id': 2, 'name': 'Third Officer', 'role': 'officer',
                'groups': {GroupIdentity.AUTHORITY},
                'ideology': Ideology.LIBERAL,
                'needs': {'power': Need('power', 70), 'manipulation': Need('manipulation', 80)},
                'influence': 70, 'speaking_ability': 85
            },
            {
                'id': 3, 'name': 'English Sailor', 'role': 'worker',
                'groups': {GroupIdentity.WORKERS},
                'ideology': Ideology.REFORMIST,
                'needs': {
                    'wage': Need('wage', 40),
                    'safety': Need('safety', 50),
                    'warmth': Need('warmth', 45)
                },
                'influence': 40, 'speaking_ability': 50
            },
            {
                'id': 4, 'name': 'Mexican Sailor', 'role': 'worker',
                'groups': {GroupIdentity.WORKERS, GroupIdentity.INDIGENOUS},
                'ideology': Ideology.REVOLUTIONARY,
                'needs': {
                    'wage': Need('wage', 25),
                    'equality': Need('equality', 20),
                    'language_rights': Need('language_rights', 30)
                },
                'influence': 35, 'speaking_ability': 45
            },
            {
                'id': 5, 'name': 'Woman Passenger', 'role': 'passenger',
                'groups': {GroupIdentity.WOMEN},
                'ideology': Ideology.LIBERAL,
                'needs': {
                    'warmth': Need('warmth', 30),
                    'equality': Need('equality', 40),
                    'safety': Need('safety', 60)
                },
                'influence': 45, 'speaking_ability': 60
            },
            {
                'id': 6, 'name': 'Native Sailor', 'role': 'worker',
                'groups': {GroupIdentity.INDIGENOUS, GroupIdentity.WORKERS},
                'ideology': Ideology.REVOLUTIONARY,
                'needs': {
                    'reparations': Need('reparations', 10),
                    'autonomy': Need('autonomy', 20),
                    'wage': Need('wage', 35)
                },
                'influence': 30, 'speaking_ability': 40
            },
            {
                'id': 7, 'name': 'Lostromo', 'role': 'worker',
                'groups': {GroupIdentity.LGBTQ, GroupIdentity.WORKERS},
                'ideology': Ideology.LIBERAL,
                'needs': {
                    'dignity': Need('dignity', 40),
                    'acceptance': Need('acceptance', 35),
                    'wage': Need('wage', 45)
                },
                'influence': 38, 'speaking_ability': 55
            },
            {
                'id': 8, 'name': 'Animal Rights Activist', 'role': 'passenger',
                'groups': {GroupIdentity.RELIGIOUS},
                'ideology': Ideology.LIBERAL,
                'needs': {
                    'animal_welfare': Need('animal_welfare', 25),
                    'morality': Need('morality', 50)
                },
                'influence': 25, 'speaking_ability': 65
            },
            {
                'id': 9, 'name': 'Professor', 'role': 'intellectual',
                'groups': {GroupIdentity.INTELLECTUALS},
                'ideology': Ideology.REVOLUTIONARY,
                'needs': {
                    'justice': Need('justice', 30),
                    'revolution': Need('revolution', 40)
                },
                'influence': 60, 'speaking_ability': 90
            },
            {
                'id': 10, 'name': 'Steward', 'role': 'steward',
                'groups': {GroupIdentity.WORKERS},
                'ideology': Ideology.ANARCHIST,
                'needs': {
                    'survival': Need('survival', 70),
                    'truth': Need('truth', 60)
                },
                'influence': 20, 'speaking_ability': 70
            }
        ]

        for template in char_templates:
            char = Character(
                id=template['id'],
                name=template['name'],
                role=template['role'],
                groups=template['groups'],
                ideology=template['ideology'],
                needs=template['needs'],
                influence=template['influence'],
                speaking_ability=template['speaking_ability']
            )
            self.characters.append(char)

    def _setup_power_structure(self):
        """Initialize power hierarchy"""
        captain = next(c for c in self.characters if c.role == 'captain')
        officers = [c.id for c in self.characters if c.role == 'officer']
        workers = [c.id for c in self.characters if c.role == 'worker']

        self.power_structure = PowerStructure(
            official_leader=captain.id,
            officers=officers,
            workers=workers,
            actual_power_rankings={}
        )

    def _initialize_character_systems(self):
        """Setup character-specific systems"""
        for char in self.characters:
            self.ethical_system.initialize_character(char.id, char.ideology)
            char.trust_in_captain = 70.0

            # Initialize trust network
            for other in self.characters:
                if other.id != char.id:
                    base_trust = 50.0
                    # Higher trust for same ideology
                    if other.ideology == char.ideology:
                        base_trust += 20
                    # Higher trust for same groups
                    if char.groups & other.groups:
                        base_trust += 15

                    char.trust_network[other.id] = base_trust

    def _create_golden_age_myth(self):
        """The beginning seems better in retrospect"""
        self.collective_memory.create_golden_age_myth(
            "Remember when we first set sail? Things were better then..."
        )

    def simulate_day(self) -> bool:
        """Main simulation loop for one day"""
        print(f"\n{'=' * 70}")
        print(f"DAY {self.day}")
        print(f"{'=' * 70}")

        # Display status
        self._display_status()

        # Ship drifts north
        self._ship_movement()

        # Environmental effects
        self._apply_environmental_effects()

        # Resource consumption
        self._manage_resources()

        # Health updates
        death_occurred = self._update_health()

        # Character daily updates
        self._update_characters()

        # Generate events
        self._generate_events()

        # Social dynamics
        self._update_social_dynamics()

        # Check for major events
        self._check_protests()
        self._check_mutiny()
        self._check_philosophical_crisis()

        # Narrative progression
        self._progress_narratives()

        # Check win/lose conditions
        if self._check_sinking():
            return False

        if self._check_salvation():
            return False

        # Advance day
        self.day += 1
        self.event_generator.decrement_cooldowns()

        return True

    def _display_status(self):
        """Display current state"""
        danger_level = self.danger_system.calculate_danger_level(
            self.heading, self.temperature
        )

        print(f"🧭 Heading: {self.heading}° ({'NORTH-DANGER' if self.heading < 90 else 'SOUTH-SAFETY'})")
        print(f"🌡️  Temperature: {self.temperature:.1f}°C")
        print(f"⚠️  Danger Level: {danger_level:.1f}/100")
        print(f"🚢 Ship Integrity: {self.danger_system.ship_integrity:.1f}/100")
        print(f"👑 Captain Authority: {self.captain_authority:.1f}/100")
        print(f"🤝 Social Cohesion: {self.social_cohesion:.1f}/100")
        print(f"💭 Philosophical Tension: {self.philosophical_tension:.1f}/100")

        alive_count = sum(1 for c in self.characters if c.is_alive)
        print(f"👥 Alive: {alive_count}/{len(self.characters)}")

        critical_resources = self.resource_system.get_critical_resources()
        if critical_resources:
            print(f"📦 Critical Resources: {', '.join(critical_resources)}")

    def _ship_movement(self):
        """Ship continues north"""
        self.heading = max(0, self.heading - CONFIG.DAILY_NORTH_DRIFT)
        self.temperature -= CONFIG.TEMPERATURE_DROP_RATE

    def _apply_environmental_effects(self):
        """Cold affects characters"""
        for char in self.characters:
            if not char.is_alive:
                continue

            if 'warmth' in char.needs:
                char.update_needs({'warmth': -self.temperature / 10})

            if self.temperature < 5:
                char.stress += 2
                char.emotional_state.fear += 1

    def _manage_resources(self):
        """Daily resource management"""
        alive_count = sum(1 for c in self.characters if c.is_alive)
        self.resource_system.daily_consumption(alive_count, self.temperature)

        # Resource crisis
        if self.resource_system.resource_crisis() and random.random() < 0.3:
            print("\n⚠️  RESOURCE CRISIS!")
            self.resource_system.activate_rationing()

    def _update_health(self) -> bool:
        """Update diseases and check deaths"""
        medicine_available = not self.resource_system.resources['medicine'].is_depleted()

        death_occurred = self.health_system.daily_health_update(
            self.characters,
            medicine_available,
            self.temperature,
            self.day
        )

        # Disease spread
        network = SocialNetwork(self.characters)
        self.health_system.spread_disease(
            self.characters,
            network.adjacency,
            self.day
        )

        # Check outbreak
        self.health_system.check_outbreak()

        return death_occurred

    def _update_characters(self):
        """Daily character updates"""
        for char in self.characters:
            if not char.is_alive:
                continue

            char.daily_update(self.day)

            # Check PTSD triggers
            if random.random() < 0.1:
                recent_event = self.event_generator.event_history[-1] if self.event_generator.event_history else None
                if recent_event:
                    triggered = char.ptsd.check_trigger(recent_event.description, self.day)
                    if triggered:
                        print(f"  😰 {char.name} triggered by memory of trauma")
                        char.stress += 20
                        char.emotional_state.fear += 15

    def _generate_events(self):
        """Generate random events"""
        danger_level = self.danger_system.calculate_danger_level(
            self.heading, self.temperature
        )

        # Random incident
        incident = self.event_generator.generate_random_incident(
            self.characters, self.day, danger_level
        )

        if incident:
            self._process_event(incident)

        # Danger event
        danger_event = self.danger_system.check_for_danger_event(
            danger_level, self.day
        )

        if danger_event:
            print(f"\n🌊 DANGER: {danger_event.danger_type.value} detected!")
            print(f"   Severity: {danger_event.severity:.1f}")

    def _process_event(self, event: Event):
        """Process an event and its effects"""
        print(f"\n🔔 EVENT: {event.description}")

        # Record event
        self.event_generator.record_event(event)

        # Characters remember differently
        for char in self.characters:
            if not char.is_alive:
                continue

            # Affected groups remember more vividly
            if any(g in event.affected_groups for g in char.groups):
                interpretation = self._generate_interpretation(char, event)
                char.add_memory(
                    self.day,
                    event.description,
                    interpretation,
                    event.severity,
                    [c.id for c in self.characters if c.is_alive and random.random() < 0.6]
                )

                print(f"  💭 {char.name}: \"{interpretation}\"")

        # Update Overton window
        self.overton_window.normalize_behavior(
            event.event_type.value,
            self.event_generator.event_counts[event.event_type],
            self.day
        )

        # Add to collective memory
        self.collective_memory.add_event_narrative(
            event.description,
            event.instigator_id if event.instigator_id else 0,
            f"The {event.event_type.value} that changed everything",
            50.0
        )

    def _generate_interpretation(self, char: Character, event: Event) -> str:
        """Generate character-specific interpretation"""
        templates = {
            Ideology.AUTHORITARIAN: f"This disrupts order. Authority must respond firmly.",
            Ideology.REVOLUTIONARY: f"This is the system failing us. We must revolt!",
            Ideology.LIBERAL: f"This violates rights. We need reforms.",
            Ideology.CONSERVATIVE: f"This shows moral decay. Return to tradition.",
            Ideology.REFORMIST: f"This proves we need gradual change.",
            Ideology.ANARCHIST: f"All hierarchy leads to this. Tear it down.",
            Ideology.NIHILIST: f"Nothing matters anyway."
        }

        return templates.get(char.ideology, "This is concerning.")

    def _update_social_dynamics(self):
        """Update alliances, networks, culture"""
        # Alliance formation
        if random.random() < CONFIG.ALLIANCE_FORMATION_CHANCE:
            self._attempt_alliance_formation()

        # Cultural evolution
        if self.day % 7 == 0:  # Weekly
            self._evolve_culture()

        # Emotional contagion
        self._spread_emotions()

    def _attempt_alliance_formation(self):
        """Characters form alliances"""
        alive_chars = [c for c in self.characters if c.is_alive]
        if len(alive_chars) < 2:
            return

        char1 = random.choice(alive_chars)
        char2 = random.choice([c for c in alive_chars if c.id != char1.id])

        # Check compatibility
        compatibility = 0.0
        if char1.ideology == char2.ideology:
            compatibility += 40
        if char1.groups & char2.groups:
            compatibility += 30
        if char1.trust_network.get(char2.id, 0) > 60:
            compatibility += 30

        if compatibility > 60:
            char1.alliances.add(char2.id)
            char2.alliances.add(char1.id)
            print(f"  🤝 {char1.name} and {char2.name} formed an alliance")

    def _evolve_culture(self):
        """Cultural norms shift"""
        print("\n📚 CULTURAL EVOLUTION:")

        # Check what behaviors have become normalized
        for behavior, level in self.overton_window.behaviors.items():
            if level == AcceptabilityLevel.POLICY:
                norm_name = f"accepting_{behavior}"
                existing = any(n.name == norm_name for n in self.cultural_evolution.norms)
                if not existing:
                    self.cultural_evolution.introduce_norm(norm_name, 80.0, self.day)
                    print(f"  ✨ New norm established: {norm_name}")

    def _spread_emotions(self):
        """Emotions spread through network"""
        for char in self.characters:
            if not char.is_alive:
                continue

            dominant_emotion, intensity = char.emotional_state.get_dominant_emotion()

            if intensity > 70:
                # Strong emotion spreads
                for ally_id in char.alliances:
                    ally = next((c for c in self.characters if c.id == ally_id), None)
                    if ally and ally.is_alive:
                        spread_amount = EmotionalContagion.spread_emotion(
                            char, ally, dominant_emotion, intensity,
                            char.trust_network.get(ally_id, 50) / 100
                        )
                        ally.emotional_state.modify_emotion(dominant_emotion, spread_amount)

    def _check_protests(self):
        """Check if protest should occur"""
        critical_needs_count = sum(
            1 for char in self.characters
            if char.is_alive and char.get_critical_needs() and char.role != 'captain'
        )

        avg_stress = sum(c.stress for c in self.characters if c.is_alive) / max(1, sum(
            1 for c in self.characters if c.is_alive))

        if critical_needs_count >= 3 and avg_stress > CONFIG.PROTEST_THRESHOLD:
            self._organize_protest()

    def _organize_protest(self):
        """Protest event"""
        print(f"\n⚠️  PROTEST ORGANIZED!")
        self.protests_held += 1

        protesters = [c for c in self.characters
                      if c.is_alive and c.role != 'captain' and c.get_critical_needs()]

        if not protesters:
            return

        print(f"  Protesters: {', '.join(p.name for p in protesters)}")

        # Collect demands
        demands = set()
        for protester in protesters:
            demands.update(protester.get_critical_needs())
            print(f"  {protester.name} demands: {', '.join(protester.get_critical_needs())}")

        # Officer manipulation
        officer = next((c for c in self.characters if c.role == 'officer' and c.is_alive), None)
        if officer:
            print(f"\n  {officer.name}: 'Continue protesting peacefully. Change will come.'")

            # Propaganda
            message = Propaganda.craft_message(
                officer,
                RhetoricTechnique.PATHOS,
                "your concerns are valid",
                protesters
            )

        # Captain makes concessions
        self._captain_concessions(demands, protesters)

        # Steward's warning
        self._steward_warning()

    def _captain_concessions(self, demands: Set[str], protesters: List):
        """Captain grants some demands"""
        concession_count = min(len(demands), random.randint(1, 3))
        granted = random.sample(list(demands), concession_count)

        print(f"\n  ✅ CAPTAIN GRANTS: {', '.join(granted)}")
        self.concessions_granted += 1

        # Apply concessions
        for protester in protesters:
            for concession in granted:
                if concession in protester.needs:
                    protester.update_needs({concession: 15})
            protester.stress -= 10

        # But captain loses authority
        self.captain_authority -= 8

        # Ship STILL heads north
        print(f"  ⚠️  However, the ship continues north into danger...")

    def _steward_warning(self):
        """Steward tries to warn everyone"""
        steward = next((c for c in self.characters if 'steward' in c.name.lower() and c.is_alive), None)
        if not steward:
            return

        print(f"\n  {steward.name}: 'These concessions mean NOTHING if we all drown!'")
        print(f"  {steward.name}: 'We must turn the ship SOUTH!'")
        print(f"  Others: 'Fascist! Counter-revolutionary!'")

        steward.stress += 15
        steward.influence -= 5

        # Others dismiss him
        for char in self.characters:
            if char.is_alive and char.id != steward.id:
                char.trust_network[steward.id] = max(0, char.trust_network.get(steward.id, 50) - 10)

    def _check_mutiny(self):
        """Check for mutiny attempt"""
        if self.captain_authority > 40:
            return

        revolutionary_count = sum(
            1 for c in self.characters
            if c.is_alive and c.ideology in [Ideology.REVOLUTIONARY, Ideology.ANARCHIST]
            and c.stress > CONFIG.MUTINY_THRESHOLD
        )

        if revolutionary_count >= 3:
            self._attempt_mutiny()

    def _attempt_mutiny(self):
        """Mutiny event"""
        print(f"\n🔥 MUTINY ATTEMPT!")
        self.mutinies_attempted += 1

        mutineers = [c for c in self.characters
                     if c.is_alive and c.ideology in [Ideology.REVOLUTIONARY, Ideology.ANARCHIST]
                     and c.role != 'captain']

        print(f"  Mutineers: {', '.join(m.name for m in mutineers)}")

        # Calculate support
        support_count = sum(1 for c in self.characters
                            if c.is_alive and c.trust_in_captain < 30 and c.role != 'captain')

        total_alive = sum(1 for c in self.characters if c.is_alive)

        if support_count > total_alive / 2:
            print(f"  ✅ MUTINY SUCCEEDS!")
            self._successful_mutiny(mutineers)
        else:
            print(f"  ❌ MUTINY FAILS! Not enough support.")
            self._failed_mutiny(mutineers)

    def _successful_mutiny(self, mutineers: List):
        """Mutiny succeeds"""
        captain = next((c for c in self.characters if c.role == 'captain'), None)
        if captain:
            captain.is_alive = False
            print(f"  💀 {captain.name} has been overthrown!")

        self.captain_authority = 0

        # New leader
        new_leader = max(mutineers, key=lambda c: c.influence)
        print(f"  👑 {new_leader.name} takes command!")

        if self.power_structure:
            self.power_structure.power_transition(captain.id if captain else 0, new_leader.id)

        # Ship turns south!
        print(f"  🔄 SHIP TURNS SOUTH!")
        self.heading = 180

        # Moral consequences
        self.overton_window.shift_window('violence', 2, self.day)
        self.ethical_system.collective_guilt += 30

    def _failed_mutiny(self, mutineers: List):
        """Mutiny fails"""
        # Mutineers suffer
        for mutineer in mutineers:
            mutineer.stress += 20
            mutineer.influence -= 15

            # May be punished
            if random.random() < 0.3:
                mutineer.is_alive = False
                print(f"  💀 {mutineer.name} was executed for mutiny")

        # Overton window shifts
        self.overton_window.shift_window('execution', 1, self.day)

    def _check_philosophical_crisis(self):
        """Check for existential discussions"""
        if self.philosophical_tension > 70 or random.random() < CONFIG.PHILOSOPHICAL_DISCUSSION_CHANCE:
            self._philosophical_discussion()

    def _philosophical_discussion(self):
        """Characters debate meaning"""
        question = random.choice([
            "What is the meaning of this voyage?",
            "Is God punishing us?",
            "What is justice?",
            "Do we have free will?",
            "Is suffering necessary?"
        ])

        print(f"\n💭 PHILOSOPHICAL DISCUSSION: '{question}'")

        speakers = random.sample(
            [c for c in self.characters if c.is_alive and c.speaking_ability > 50],
            min(3, sum(1 for c in self.characters if c.is_alive))
        )

        for speaker in speakers:
            perspective = self._get_philosophical_perspective(speaker, question)
            print(f"  {speaker.name}: {perspective}")
            speaker.influence += 2

        self.philosophical_tension += random.uniform(5, 15)

        # May affect beliefs
        for char in self.characters:
            if char.is_alive and random.random() < 0.2:
                char.belief_system.doubt_level += 5

    def _get_philosophical_perspective(self, char: Character, question: str) -> str:
        """Get character's philosophical view"""
        perspectives = {
            Ideology.AUTHORITARIAN: "Order and hierarchy are the meaning of existence.",
            Ideology.REVOLUTIONARY: "We create meaning through struggle and liberation.",
            Ideology.CONSERVATIVE: "Traditional values give life purpose.",
            Ideology.LIBERAL: "Individual rights and dignity are paramount.",
            Ideology.ANARCHIST: "Freedom from all authority is the only truth.",
            Ideology.NIHILIST: "There is no inherent meaning. All is void."
        }
        return perspectives.get(char.ideology, "I'm not sure.")

    def _progress_narratives(self):
        """Progress character story arcs"""
        for char_id, arc in self.narrative_engine.story_arcs.items():
            if arc.completed:
                continue

            char = next((c for c in self.characters if c.id == char_id), None)
            if not char or not char.is_alive:
                continue

            # Progress based on recent events
            if self.event_generator.event_history:
                recent = self.event_generator.event_history[-1]
                if recent.instigator_id == char_id or recent.target_id == char_id:
                    arc.advance_arc(recent.description, 10.0)

        # Check for Chekhov's gun
        payoff = self.narrative_engine.check_chekovs_gun(self.day)
        if payoff:
            print(f"\n📖 FORESHADOWING PAYS OFF: {payoff['payoff']}")

    def _check_sinking(self) -> bool:
        """Check if ship sinks"""
        danger_level = self.danger_system.calculate_danger_level(
            self.heading, self.temperature
        )

        if self.danger_system.check_sinking_conditions(danger_level):
            self._ship_sinks()
            return True

        return False

    def _ship_sinks(self):
        """GAME OVER - Ship sinks"""
        print(f"\n{'=' * 70}")
        print(f"💀 THE SHIP HITS ICEBERGS AND SINKS!")
        print(f"{'=' * 70}")
        print(f"\n🌊 Everyone drowns.\n")

        print(f"The ship traveled {360 - self.heading}° north into danger.")
        print(f"\nWhile passengers argued about:")

        all_demands = set()
        for char in self.characters:
            all_demands.update(char.get_critical_needs())

        for demand in all_demands:
            print(f"  • {demand}")

        print(f"\n...nobody listened to warnings to turn south.\n")

        self._print_final_statistics()

        self.simulation_active = False

    def _check_salvation(self) -> bool:
        """Check if ship is saved (rare)"""
        if self.heading >= 160:  # Almost south
            alive_count = sum(1 for c in self.characters if c.is_alive)
            if alive_count >= len(self.characters) * 0.7:  # 70% survived
                self._ship_saved()
                return True
        return False

    def _ship_saved(self):
        """RARE ENDING - Ship is saved"""
        print(f"\n{'=' * 70}")
        print(f"🎉 THE SHIP TURNED SOUTH AND WAS SAVED!")
        print(f"{'=' * 70}")
        print(f"\nAgainst all odds, reason prevailed.\n")

        print(f"The ship turned {self.heading}° from danger.")
        print(f"Lives saved: {sum(1 for c in self.characters if c.is_alive)}/{len(self.characters)}")

        self._print_final_statistics()

        self.simulation_active = False

    def _print_final_statistics(self):
        """Print end game stats"""
        print(f"\n📊 FINAL STATISTICS:")
        print(f"  Days survived: {self.day}")
        print(f"  Protests held: {self.protests_held}")
        print(f"  Concessions granted: {self.concessions_granted}")
        print(f"  Mutinies attempted: {self.mutinies_attempted}")
        print(f"  Final captain authority: {self.captain_authority:.1f}/100")
        print(f"  Final ship integrity: {self.danger_system.ship_integrity:.1f}/100")

        alive = [c for c in self.characters if c.is_alive]
        print(f"\n👥 SURVIVORS ({len(alive)}):")
        for char in alive:
            print(f"  • {char.name} ({char.ideology.value})")

        dead = [c for c in self.characters if not c.is_alive]
        if dead:
            print(f"\n💀 CASUALTIES ({len(dead)}):")
            for char in dead:
                print(f"  • {char.name}")

        print(f"\n🎭 CULTURAL SHIFTS:")
        for behavior, level in self.overton_window.behaviors.items():
            if level != AcceptabilityLevel.UNTHINKABLE:
                print(f"  • {behavior}: {level.value}")

        print(f"\n⚖️  COLLECTIVE GUILT: {self.ethical_system.collective_guilt:.1f}/100")

    def print_detailed_status(self):
        """Detailed status report"""
        print(f"\n{'=' * 70}")
        print(f"📊 DETAILED STATUS REPORT - DAY {self.day}")
        print(f"{'=' * 70}")

        print(f"\n👥 CHARACTER STATUS:")
        for char in self.characters:
            if not char.is_alive:
                print(f"\n  💀 {char.name} - DECEASED")
                continue

            print(f"\n  {char.name} ({char.role})")
            print(f"    Ideology: {char.ideology.value}")
            print(f"    Groups: {', '.join(g.value for g in char.groups)}")
            print(f"    Satisfaction: {char.calculate_satisfaction():.1f}/100")
            print(f"    Stress: {char.stress:.1f}/100")
            print(f"    Influence: {char.influence:.1f}/100")
            print(f"    Trust in captain: {char.trust_in_captain:.1f}/100")

            dominant_emotion, intensity = char.emotional_state.get_dominant_emotion()
            print(f"    Dominant emotion: {dominant_emotion} ({intensity:.1f})")

            if char.is_radicalized:
                print(f"    ⚠️  RADICALIZED")

            critical = char.get_critical_needs()
            if critical:
                print(f"    ⚠️  Critical needs: {', '.join(critical)}")

            if char.alliances:
                print(f"    Allies: {len(char.alliances)}")

            # PTSD
            ptsd_score = char.ptsd.calculate_total_impact(self.day)
            if ptsd_score > 30:
                print(f"    😰 PTSD impact: {ptsd_score:.1f}")

        print(f"\n🤝 ALLIANCES:")
        active_alliances = self.alliance_network.get_active_alliances()
        if active_alliances:
            for i, alliance in enumerate(active_alliances):
                members = [c.name for c in self.characters if c.id in alliance.members and c.is_alive]
                print(f"  {i + 1}. {', '.join(members)}")
                print(f"     Type: {alliance.alliance_type.value}")
                print(f"     Strength: {alliance.strength:.1f}/100")
                if alliance.radicalization_level > 50:
                    print(f"     ⚠️  Radicalized ({alliance.radicalization_level:.1f})")
        else:
            print(f"  No active alliances")

        print(f"\n📦 RESOURCES:")
        for name, resource in self.resource_system.resources.items():
            status = "⚠️ CRITICAL" if resource.is_critical() else "✓"
            print(f"  {status} {name}: {resource.quantity:.1f}")

        if self.resource_system.rationing_active:
            print(f"  📋 RATIONING ACTIVE")
        if self.resource_system.black_market_active:
            print(f"  💰 BLACK MARKET EXISTS")

        print(f"\n🏥 HEALTH:")
        if self.health_system.sick_characters:
            for char_id, conditions in self.health_system.sick_characters.items():
                char = next((c for c in self.characters if c.id == char_id), None)
                if char:
                    print(f"  {char.name}:")
                    for condition in conditions:
                        print(f"    • {condition.disease.value} (severity: {condition.severity:.1f})")
        else:
            print(f"  No active illnesses")

        if self.health_system.outbreak_active:
            print(f"  🦠 EPIDEMIC: {', '.join(d.value for d in self.health_system.epidemic_diseases)}")

        print(f"\n📖 RECENT EVENTS:")
        recent = self.event_generator.event_history[-5:]
        for event in recent:
            print(f"  Day {event.day}: {event.description}")

        print(f"\n🎭 OVERTON WINDOW SHIFTS:")
        shifts = [h for h in self.overton_window.shift_history[-5:]]
        for shift in shifts:
            print(f"  Day {shift['day']}: {shift['behavior']}: {shift['from']} → {shift['to']}")


# ==================================================
# FILE 22: main.py
# ==================================================

def main():
    """Main entry point"""
    print("=" * 70)
    print("🚢 SHIP OF FOOLS - ADVANCED SOCIAL SIMULATION")
    print("=" * 70)
    print("\nBased on Theodore Kaczynski's allegory")
    print("\nThe ship heads north into dangerous waters...")
    print("Will anyone listen to reason before it's too late?\n")

    # Initialize ship
    ship = Ship()
    ship.initialize()

    print("✓ Ship initialized")
    print(f"✓ {len(ship.characters)} characters created")
    print(f"✓ All systems operational\n")

    # Simulation loop
    try:
        while ship.simulation_active:
            if not ship.simulate_day():
                break

            # Detailed status every 5 days
            if ship.day % 5 == 0:
                ship.print_detailed_status()

            # Check if we've exceeded max days
            if ship.day > CONFIG.MAX_DAYS:
                print(f"\n⏰ Maximum simulation days reached")
                break

            # Pause for user input
            response = input("\n[Press ENTER to continue, 's' for status, 'q' to quit]: ").strip().lower()

            if response == 'q':
                print("\nSimulation ended by user.")
                break
            elif response == 's':
                ship.print_detailed_status()

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")

    # Final summary
    print("\n" + "=" * 70)
    print("📖 SIMULATION COMPLETE")
    print("=" * 70)

    print("\n🎯 KEY LESSONS FROM THIS SIMULATION:")
    print("  • Groups focused on immediate grievances while ignoring existential threats")
    print("  • Authority manipulated through small, meaningless concessions")
    print("  • Those warning about real danger were dismissed as extremists")
    print("  • Conflicting memories and narratives prevented unified action")
    print("  • Cultural norms shifted to accept previously unthinkable behaviors")
    print("  • The ship sank while everyone argued about distribution of resources")

    print("\n💭 REFLECTION:")
    print("  This simulation demonstrates how social psychology, power structures,")
    print("  and cognitive biases can lead groups toward collective disaster even")
    print("  when the solution is obvious to any rational observer.")

    print("\n📚 SYSTEMS DEMONSTRATED:")
    print("  ✓ Psychological (personality, trauma, PTSD, emotion, cognition)")
    print("  ✓ Social (alliances, networks, propaganda, culture)")
    print("  ✓ Power (hierarchy, manipulation, politics)")
    print("  ✓ Morality (Overton window, ethics, dilemmas)")
    print("  ✓ Narrative (story arcs, memory, foreshadowing)")
    print("  ✓ Environmental (resources, health, danger)")

    print("\n" + "=" * 70)
    print("Thank you for experiencing the Ship of Fools.")
    print("=" * 70)


if __name__ == "__main__":
    main()

# ==================================================
# COMPLETE PROJECT STRUCTURE
# ==================================================

print("\n\n" + "=" * 70)
print("🎉 SHIP OF FOOLS - COMPLETE SYSTEM")
print("=" * 70)
print("\n✅ ALL MODULES IMPLEMENTED:")
print("\n📁 Configuration & Core:")
print("  ✓ config.py - All enums and settings")
print("  ✓ core/character.py - Enhanced character system")
print("  ✓ core/ship.py - Main ship class with full integration")
print("  ✓ core/event.py - Dynamic event generation")
print("\n🧠 Psychology Systems:")
print("  ✓ psychology/personality.py - Big Five traits")
print("  ✓ psychology/trauma.py - Trauma & PTSD")
print("  ✓ psychology/emotion.py - Emotional contagion")
print("  ✓ psychology/cognition.py - Cognitive biases")
print("\n👥 Social Systems:")
print("  ✓ social/alliance.py - Alliance dynamics")
print("  ✓ social/network.py - Network analysis")
print("  ✓ social/communication.py - Rhetoric & propaganda")
print("  ✓ social/culture.py - Cultural evolution")
print("\n⚡ Power Systems:")
print("  ✓ power/hierarchy.py - Power structures")
print("  ✓ power/manipulation.py - Manipulation tactics")
print("\n⚖️  Morality Systems:")
print("  ✓ morality/overton.py - Overton window")
print("  ✓ morality/ethics.py - Ethical frameworks")
print("\n📖 Narrative Systems:")
print("  ✓ narrative/story.py - Story arcs")
print("  ✓ narrative/memory.py - Collective memory")
print("\n🌊 Environment Systems:")
print("  ✓ environment/resources.py - Resource management")
print("  ✓ environment/health.py - Disease system")
print("  ✓ environment/danger.py - Environmental dangers")
print("\n🎮 Main Application:")
print("  ✓ main.py - Complete simulation engine")
print("\n" + "=" * 70)
print("🚀 TO RUN: python main.py")
print("=" * 70)
print("\nFEATURES:")
print("  • 10 unique characters with psychological depth")
print("  • Real-time personality changes and radicalization")
print("  • Trauma and PTSD simulation")
print("  • Dynamic alliance formation and betrayal")
print("  • Propaganda and emotional contagion")
print("  • Overton window normalization")
print("  • Resource scarcity and disease outbreaks")
print("  • Multiple possible endings")
print("  • Detailed narrative tracking")
print("  • Social network analysis")
print("  • Moral dilemmas and ethical decay")
print("\n💡 This is a complete, working simulation ready to run!")
print("=" * 70)
"""
═══════════════════════════════════════════════════════════════════════════════
                            SHIP OF FOOLS
                    Advanced Social Simulation System
                Based on Theodore Kaczynski's Allegory
═══════════════════════════════════════════════════════════════════════════════

ABOUT:
------
This simulation demonstrates how groups prioritize immediate grievances over
existential threats, how authority manipulates through small concessions, and
how those warning about real danger are dismissed as extremists.

SYSTEMS IMPLEMENTED:
-------------------
✓ Psychology: Personality traits, trauma, PTSD, emotions, cognitive biases
✓ Social: Alliances, social networks, propaganda, cultural evolution  
✓ Power: Hierarchies, manipulation tactics, political maneuvering
✓ Morality: Overton window, ethical frameworks, moral decay
✓ Narrative: Story arcs, collective memory, foreshadowing
✓ Environment: Resources, disease outbreaks, environmental dangers

USAGE:
------
1. Run: python ship_of_fools.py
2. Press ENTER to advance day by day
3. Type 's' for detailed status report
4. Type 'q' to quit simulation

The ship heads north into danger while passengers argue about trivial matters.
Will anyone listen to the steward's warnings before it's too late?

═══════════════════════════════════════════════════════════════════════════════
"""

import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict

# ==================================================
# CONFIGURATION & ENUMS
# ==================================================

from enum import Enum
from dataclasses import dataclass


class Ideology(Enum):
    AUTHORITARIAN = "authoritarian"
    REFORMIST = "reformist"
    REVOLUTIONARY = "revolutionary"
    CONSERVATIVE = "conservative"
    LIBERAL = "liberal"
    ANARCHIST = "anarchist"
    NIHILIST = "nihilist"


class GroupIdentity(Enum):
    AUTHORITY = "authority"
    WORKERS = "workers"
    WOMEN = "women"
    LGBTQ = "lgbtq"
    RELIGIOUS = "religious"
    INDIGENOUS = "indigenous"
    MERCHANTS = "merchants"
    INTELLECTUALS = "intellectuals"


class PersonalityTrait(Enum):
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"


class EmotionType(Enum):
    FEAR = "fear"
    ANGER = "anger"
    HOPE = "hope"
    DESPAIR = "despair"
    TRUST = "trust"
    DISGUST = "disgust"


class EventType(Enum):
    THEFT = "theft"
    FIGHT = "fight"
    PROTEST = "protest"
    MUTINY = "mutiny"
    DEATH = "death"
    DISEASE = "disease"
    SCARCITY = "scarcity"
    ABUSE = "abuse"
    NEGOTIATION = "negotiation"
    RITUAL = "ritual"


@dataclass
class Config:
    # Simulation parameters
    MAX_DAYS: int = 50
    STARTING_TEMPERATURE: float = 15.0
    STARTING_HEADING: int = 0  # North
    SAFE_HEADING: int = 180  # South

    # Thresholds
    PROTEST_THRESHOLD: float = 60.0
    MUTINY_THRESHOLD: float = 70.0
    DEATH_THRESHOLD: float = 90.0
    RADICALIZATION_THRESHOLD: float = 75.0

    # Rates
    DAILY_NORTH_DRIFT: int = 2
    TEMPERATURE_DROP_RATE: float = 0.5
    STRESS_INCREASE_RATE: float = 1.5
    TRUST_DECAY_RATE: float = 0.5

    # Game balance
    CAPTAIN_CONCESSION_RATE: float = 0.3
    ALLIANCE_FORMATION_CHANCE: float = 0.15
    EVENT_CHANCE: float = 0.25
    PHILOSOPHICAL_DISCUSSION_CHANCE: float = 0.20

    # AI/Behavior
    EMOTION_CONTAGION_RATE: float = 0.15
    PROPAGANDA_EFFECTIVENESS: float = 0.25
    OVERTON_SHIFT_RATE: float = 2.0


CONFIG = Config()

# ==================================================
# FILE 2: psychology/personality.py
# ==================================================

from dataclasses import dataclass, field
from typing import Dict
import random


@dataclass
class Personality:
    """Big Five personality model"""
    openness: float = 50.0  # 0-100
    conscientiousness: float = 50.0
    extraversion: float = 50.0
    agreeableness: float = 50.0
    neuroticism: float = 50.0

    def get_trait(self, trait: str) -> float:
        return getattr(self, trait, 50.0)

    def modify_trait(self, trait: str, amount: float):
        current = self.get_trait(trait)
        setattr(self, trait, max(0, min(100, current + amount)))

    def calculate_stress_vulnerability(self) -> float:
        """High neuroticism = more vulnerable to stress"""
        return self.neuroticism / 100

    def calculate_leadership_potential(self) -> float:
        """Leadership based on extraversion and conscientiousness"""
        return (self.extraversion * 0.6 + self.conscientiousness * 0.4) / 100

    def calculate_radicalization_susceptibility(self) -> float:
        """High openness + low agreeableness = more radical"""
        return (self.openness * 0.5 + (100 - self.agreeableness) * 0.5) / 100

    @staticmethod
    def generate_random() -> 'Personality':
        return Personality(
            openness=random.uniform(30, 90),
            conscientiousness=random.uniform(30, 90),
            extraversion=random.uniform(20, 90),
            agreeableness=random.uniform(30, 90),
            neuroticism=random.uniform(20, 80)
        )


# ==================================================
# FILE 3: psychology/trauma.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TraumaType(Enum):
    VIOLENCE = "violence"
    BETRAYAL = "betrayal"
    LOSS = "loss"
    HUMILIATION = "humiliation"
    EXISTENTIAL = "existential"


class TraumaSeverity(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    CRITICAL = 4


@dataclass
class Trauma:
    trauma_type: TraumaType
    severity: TraumaSeverity
    day_occurred: int
    description: str
    triggers: List[str] = field(default_factory=list)
    processed: bool = False
    ptsd_score: float = 0.0

    def age(self, current_day: int) -> int:
        return current_day - self.day_occurred

    def is_fresh(self, current_day: int) -> bool:
        return self.age(current_day) < 7

    def calculate_impact(self, current_day: int) -> float:
        """Trauma impact decreases over time if processed"""
        base_impact = self.severity.value * 10

        if self.processed:
            decay = 0.9 ** self.age(current_day)
            return base_impact * decay
        else:
            # Unprocessed trauma can worsen
            growth = 1.1 ** min(self.age(current_day), 20)
            return base_impact * growth


@dataclass
class PTSDSystem:
    """Post-Traumatic Stress Disorder simulation"""
    traumas: List[Trauma] = field(default_factory=list)
    flashback_triggers: Dict[str, List[Trauma]] = field(default_factory=dict)
    hypervigilance: float = 0.0  # 0-100
    emotional_numbing: float = 0.0  # 0-100

    def add_trauma(self, trauma: Trauma):
        self.traumas.append(trauma)

        # Register triggers
        for trigger in trauma.triggers:
            if trigger not in self.flashback_triggers:
                self.flashback_triggers[trigger] = []
            self.flashback_triggers[trigger].append(trauma)

        # Increase PTSD symptoms
        self.hypervigilance += trauma.severity.value * 5
        if len(self.traumas) > 3:
            self.emotional_numbing += 10

    def check_trigger(self, event_description: str, current_day: int) -> Optional[List[Trauma]]:
        """Check if event triggers flashbacks"""
        triggered = []

        for trigger, traumas in self.flashback_triggers.items():
            if trigger.lower() in event_description.lower():
                for trauma in traumas:
                    if not trauma.processed and trauma.is_fresh(current_day):
                        triggered.append(trauma)

        return triggered if triggered else None

    def calculate_total_impact(self, current_day: int) -> float:
        """Total PTSD impact on character"""
        return sum(t.calculate_impact(current_day) for t in self.traumas)

    def attempt_processing(self, trauma: Trauma, support_level: float) -> bool:
        """Attempt to process trauma with social support"""
        success_chance = support_level / 100

        if random.random() < success_chance:
            trauma.processed = True
            self.hypervigilance = max(0, self.hypervigilance - 10)
            return True
        return False


# ==================================================
# FILE 4: psychology/emotion.py
# ==================================================

from dataclasses import dataclass, field
from typing import Dict, List, Set
import random


@dataclass
class EmotionalState:
    """Character's current emotional state"""
    fear: float = 0.0  # 0-100
    anger: float = 0.0
    hope: float = 50.0
    despair: float = 0.0
    trust: float = 50.0
    disgust: float = 0.0

    def get_dominant_emotion(self) -> tuple[str, float]:
        """Returns (emotion_name, intensity)"""
        emotions = {
            'fear': self.fear,
            'anger': self.anger,
            'hope': self.hope,
            'despair': self.despair,
            'trust': self.trust,
            'disgust': self.disgust
        }
        dominant = max(emotions.items(), key=lambda x: x[1])
        return dominant

    def modify_emotion(self, emotion: str, amount: float):
        if hasattr(self, emotion):
            current = getattr(self, emotion)
            setattr(self, emotion, max(0, min(100, current + amount)))

    def decay_emotions(self, rate: float = 0.05):
        """Emotions naturally decay over time"""
        self.fear *= (1 - rate)
        self.anger *= (1 - rate)
        self.despair *= (1 - rate)
        self.disgust *= (1 - rate)

        # Hope and trust decay slower
        self.hope = max(10, self.hope * (1 - rate / 2))
        self.trust = max(10, self.trust * (1 - rate / 2))


class EmotionalContagion:
    """Emotions spread through social network"""

    @staticmethod
    def spread_emotion(source_char, target_char, emotion: str,
                       intensity: float, relationship_strength: float) -> float:
        """
        Emotions spread based on:
        - Intensity of source emotion
        - Relationship strength
        - Target's personality (neuroticism)
        """
        base_spread = intensity * relationship_strength * CONFIG.EMOTION_CONTAGION_RATE

        # Neurotic people catch emotions more easily
        susceptibility = target_char.personality.neuroticism / 100

        spread_amount = base_spread * (0.5 + susceptibility * 0.5)

        return spread_amount

    @staticmethod
    def mob_mentality(characters: List, emotion: str, threshold: float = 60.0) -> bool:
        """Check if mob mentality is triggered"""
        high_emotion_count = sum(
            1 for char in characters
            if getattr(char.emotional_state, emotion, 0) > threshold
        )

        ratio = high_emotion_count / len(characters)
        return ratio > 0.4  # 40% threshold for mob


# ==================================================
# FILE 5: psychology/cognition.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict
import random


class CognitiveBias:
    """Various cognitive biases that affect decision-making"""

    @staticmethod
    def confirmation_bias(character, new_info: str, matches_belief: bool) -> float:
        """People accept info that matches beliefs, reject contradictory"""
        if matches_belief:
            return 1.5  # Amplify confirming evidence
        else:
            # High openness = less bias
            openness = character.personality.openness / 100
            return 0.3 + (openness * 0.5)  # Reduce contradictory evidence

    @staticmethod
    def availability_heuristic(character, event_type: str) -> float:
        """Recent/dramatic events seem more likely"""
        recent_memories = [m for m in character.memories[-5:]
                           if event_type.lower() in m.event.lower()]

        if recent_memories:
            return 1.0 + (len(recent_memories) * 0.3)
        return 1.0

    @staticmethod
    def anchoring_bias(character, initial_value: float, adjustment: float) -> float:
        """First impression anchors later judgments"""
        # Low conscientiousness = more susceptible to anchoring
        susceptibility = (100 - character.personality.conscientiousness) / 100

        return initial_value + (adjustment * (0.3 + susceptibility * 0.4))

    @staticmethod
    def groupthink(alliance_members: List, dissenting_opinion: bool) -> bool:
        """Group pressure suppresses dissent"""
        if not dissenting_opinion:
            return True

        # Larger groups = more groupthink
        pressure = min(len(alliance_members) / 10, 0.9)

        return random.random() > pressure

    @staticmethod
    def sunk_cost_fallacy(character, days_invested: int) -> float:
        """More invested = harder to change course"""
        return 1.0 + (days_invested * 0.05)


@dataclass
class BeliefSystem:
    """Character's beliefs and how they change"""
    core_beliefs: Dict[str, float] = field(default_factory=dict)  # belief -> strength (0-100)
    doubt_level: float = 0.0  # 0-100
    radicalization_score: float = 0.0  # 0-100

    def add_belief(self, belief: str, strength: float = 50.0):
        self.core_beliefs[belief] = strength

    def challenge_belief(self, belief: str, evidence_strength: float,
                         character_openness: float) -> bool:
        """Attempt to change a belief"""
        if belief not in self.core_beliefs:
            return False

        current_strength = self.core_beliefs[belief]

        # Openness makes beliefs more flexible
        flexibility = character_openness / 100

        change_threshold = current_strength * (1 - flexibility * 0.5)

        if evidence_strength > change_threshold:
            # Belief shaken
            self.core_beliefs[belief] *= 0.7
            self.doubt_level += 10
            return True
        else:
            # Belief reinforced (backfire effect)
            self.core_beliefs[belief] = min(100, current_strength * 1.1)
            return False

    def radicalize(self, trauma_score: float, group_pressure: float):
        """Trauma + group pressure = radicalization"""
        radicalization_force = (trauma_score + group_pressure) / 2

        self.radicalization_score += radicalization_force * 0.1
        self.radicalization_score = min(100, self.radicalization_score)

        # Radicalization reduces doubt
        self.doubt_level *= 0.9


# ==================================================
# FILE 6: core/character.py (UPDATED WITH PSYCHOLOGY)
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import random


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

        memory = Memory(day, event, interpretation, emotional_impact,
                        witnesses, dominant_emotion)
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


# ==================================================
# FILE 7: social/alliance.py
# ==================================================

from dataclasses import dataclass, field
from typing import Set, List, Optional
from enum import Enum
import random


class AllianceType(Enum):
    IDEOLOGICAL = "ideological"  # Shared beliefs
    IDENTITY = "identity"  # Shared group identity
    PRAGMATIC = "pragmatic"  # Mutual benefit
    PROTECTION = "protection"  # Safety in numbers
    REVOLUTIONARY = "revolutionary"  # Overthrow authority


@dataclass
class Alliance:
    members: Set[int]
    alliance_type: AllianceType
    purpose: str
    strength: float = 50.0
    created_day: int = 0
    leader_id: Optional[int] = None
    broken: bool = False
    secrecy_level: float = 0.0  # 0=public, 100=secret conspiracy

    # Alliance dynamics
    internal_trust: float = 70.0
    cohesion: float = 60.0
    radicalization_level: float = 0.0

    def add_member(self, char_id: int):
        self.members.add(char_id)
        self.strength += 5
        # New members lower average trust temporarily
        self.internal_trust *= 0.95

    def remove_member(self, char_id: int):
        self.members.discard(char_id)
        self.strength -= 15
        self.internal_trust -= 10

        if len(self.members) < 2:
            self.broken = True

    def elect_leader(self, characters: List) -> int:
        """Elect most influential member as leader"""
        member_chars = [c for c in characters if c.id in self.members and c.is_alive]
        if not member_chars:
            self.broken = True
            return None

        leader = max(member_chars, key=lambda c: c.influence)
        self.leader_id = leader.id
        return leader.id

    def calculate_power(self, characters: List) -> float:
        """Alliance power = members * average influence * cohesion"""
        member_chars = [c for c in characters if c.id in self.members and c.is_alive]
        if not member_chars:
            return 0.0

        avg_influence = sum(c.influence for c in member_chars) / len(member_chars)
        return len(member_chars) * avg_influence * (self.cohesion / 100)

    def radicalize(self, amount: float):
        """Alliance becomes more radical"""
        self.radicalization_level += amount
        self.radicalization_level = min(100, self.radicalization_level)

        if self.radicalization_level > 70:
            self.alliance_type = AllianceType.REVOLUTIONARY
            self.secrecy_level += 10


class AllianceNetwork:
    """Manages all alliances on the ship"""

    def __init__(self):
        self.alliances: List[Alliance] = []
        self.history: List[str] = []

    def create_alliance(self, members: Set[int], alliance_type: AllianceType,
                        purpose: str, day: int) -> Alliance:
        alliance = Alliance(
            members=members,
            alliance_type=alliance_type,
            purpose=purpose,
            created_day=day
        )
        self.alliances.append(alliance)
        self.history.append(f"Day {day}: Alliance formed - {purpose}")
        return alliance

    def find_alliance(self, char_id: int) -> Optional[Alliance]:
        """Find alliance that character belongs to"""
        for alliance in self.alliances:
            if char_id in alliance.members and not alliance.broken:
                return alliance
        return None

    def merge_alliances(self, alliance1: Alliance, alliance2: Alliance) -> Alliance:
        """Two alliances merge into one"""
        merged = Alliance(
            members=alliance1.members | alliance2.members,
            alliance_type=alliance1.alliance_type,
            purpose=f"Merged: {alliance1.purpose} & {alliance2.purpose}",
            strength=(alliance1.strength + alliance2.strength) / 2
        )

        alliance1.broken = True
        alliance2.broken = True
        self.alliances.append(merged)
        return merged

    def get_active_alliances(self) -> List[Alliance]:
        return [a for a in self.alliances if not a.broken and len(a.members) >= 2]


# ==================================================
# FILE 8: social/network.py
# ==================================================

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import math


class SocialNetwork:
    """Social network analysis for the ship"""

    def __init__(self, characters: List):
        self.characters = characters
        self.adjacency: Dict[int, Set[int]] = {}
        self._build_network()

    def _build_network(self):
        """Build network from character relationships"""
        for char in self.characters:
            self.adjacency[char.id] = set()

            # Add allies
            self.adjacency[char.id].update(char.alliances)

            # Add trust network connections
            for other_id, trust in char.trust_network.items():
                if trust > 50:
                    self.adjacency[char.id].add(other_id)

    def calculate_centrality(self, char_id: int) -> float:
        """Degree centrality - how connected is this character"""
        if char_id not in self.adjacency:
            return 0.0

        connections = len(self.adjacency[char_id])
        max_possible = len(self.characters) - 1

        return (connections / max_possible) * 100 if max_possible > 0 else 0

    def calculate_betweenness(self, char_id: int) -> float:
        """How often does this character bridge between groups"""
        # Simplified betweenness centrality
        bridges = 0
        total_paths = 0

        for source in self.adjacency:
            if source == char_id:
                continue
            for target in self.adjacency:
                if target == char_id or target == source:
                    continue

                total_paths += 1
                if self._is_on_path(source, target, char_id):
                    bridges += 1

        return (bridges / total_paths * 100) if total_paths > 0 else 0

    def _is_on_path(self, source: int, target: int, bridge: int) -> bool:
        """Simplified path checking"""
        return (bridge in self.adjacency.get(source, set()) and
                target in self.adjacency.get(bridge, set()))

    def find_clusters(self) -> List[Set[int]]:
        """Find densely connected groups"""
        visited = set()
        clusters = []

        for char_id in self.adjacency:
            if char_id in visited:
                continue

            cluster = self._dfs_cluster(char_id, visited)
            if len(cluster) >= 2:
                clusters.append(cluster)

        return clusters

    def _dfs_cluster(self, start: int, visited: Set[int]) -> Set[int]:
        """Depth-first search to find cluster"""
        cluster = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            cluster.add(node)

            for neighbor in self.adjacency.get(node, set()):
                if neighbor not in visited:
                    stack.append(neighbor)

        return cluster

    def calculate_network_density(self) -> float:
        """Overall network connectivity"""
        total_edges = sum(len(connections) for connections in self.adjacency.values())
        n = len(self.characters)
        max_edges = n * (n - 1)

        return (total_edges / max_edges * 100) if max_edges > 0 else 0

    def identify_influencers(self, top_n: int = 3) -> List[int]:
        """Find most influential characters by centrality"""
        centralities = [(char.id, self.calculate_centrality(char.id))
                        for char in self.characters if char.is_alive]

        centralities.sort(key=lambda x: x[1], reverse=True)
        return [char_id for char_id, _ in centralities[:top_n]]


# ==================================================
# FILE 9: social/communication.py
# ==================================================

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import random


class RhetoricTechnique(Enum):
    ETHOS = "ethos"  # Appeal to authority/credibility
    PATHOS = "pathos"  # Appeal to emotion
    LOGOS = "logos"  # Appeal to logic
    KAIROS = "kairos"  # Appeal to timing/urgency
    DEMAGOGY = "demagogy"  # Manipulation of masses


@dataclass
class Message:
    speaker_id: int
    content: str
    technique: RhetoricTechnique
    target_emotion: str
    day: int
    effectiveness: float = 0.0


class Propaganda:
    """Propaganda and manipulation system"""

    @staticmethod
    def craft_message(speaker, technique: RhetoricTechnique,
                      topic: str, target_audience: List) -> Message:
        """Create propaganda message"""

        templates = {
            RhetoricTechnique.ETHOS: [
                f"As your {speaker.role}, I assure you that {topic}",
                f"Trust in my experience - {topic}",
                f"The authorities agree that {topic}"
            ],
            RhetoricTechnique.PATHOS: [
                f"Think of your families! {topic}",
                f"Are you afraid? You should be, because {topic}",
                f"Together we can overcome {topic}"
            ],
            RhetoricTechnique.LOGOS: [
                f"The facts show that {topic}",
                f"Logically speaking, {topic}",
                f"Evidence demonstrates {topic}"
            ],
            RhetoricTechnique.KAIROS: [
                f"We must act NOW! {topic}",
                f"This is our only chance - {topic}",
                f"Time is running out: {topic}"
            ],
            RhetoricTechnique.DEMAGOGY: [
                f"THEY want to {topic}, but WE won't let them!",
                f"The enemy is responsible for {topic}",
                f"Only I can save you from {topic}"
            ]
        }

        content = random.choice(templates[technique])

        # Determine target emotion
        emotion_map = {
            RhetoricTechnique.ETHOS: "trust",
            RhetoricTechnique.PATHOS: random.choice(["fear", "hope", "anger"]),
            RhetoricTechnique.LOGOS: "trust",
            RhetoricTechnique.KAIROS: "fear",
            RhetoricTechnique.DEMAGOGY: "anger"
        }

        return Message(
            speaker_id=speaker.id,
            content=content,
            technique=technique,
            target_emotion=emotion_map[technique],
            day=0
        )

    @staticmethod
    def calculate_effectiveness(message: Message, speaker, audience_member) -> float:
        """How effective is propaganda on this person"""

        base_effectiveness = speaker.speaking_ability / 100

        # Personality factors
        if message.technique == RhetoricTechnique.PATHOS:
            # Emotional people more susceptible
            emotion_factor = audience_member.personality.neuroticism / 100
            base_effectiveness *= (0.7 + emotion_factor * 0.6)

        elif message.technique == RhetoricTechnique.LOGOS:
            # Logical people respond to logic
            logic_factor = audience_member.personality.openness / 100
            base_effectiveness *= (0.7 + logic_factor * 0.6)

        elif message.technique == RhetoricTechnique.DEMAGOGY:
            # Angry, stressed people vulnerable to demagogy
            vulnerability = (audience_member.stress +
                             audience_member.emotional_state.anger) / 200
            base_effectiveness *= (0.5 + vulnerability)

        # Trust in speaker
        trust_factor = audience_member.trust_network.get(speaker.id, 50) / 100
        base_effectiveness *= (0.5 + trust_factor * 0.5)

        # Cognitive bias: confirmation bias
        matches_ideology = (speaker.ideology == audience_member.ideology)
        if matches_ideology:
            base_effectiveness *= 1.5
        else:
            base_effectiveness *= 0.6

        return min(1.0, base_effectiveness)


class EchoChamber:
    """Echo chamber effect - beliefs reinforce within groups"""

    def __init__(self):
        self.chambers: Dict[str, List[int]] = {}  # ideology -> char_ids

    def add_to_chamber(self, char_id: int, ideology: str):
        if ideology not in self.chambers:
            self.chambers[ideology] = []
        if char_id not in self.chambers[ideology]:
            self.chambers[ideology].append(char_id)

    def amplify_beliefs(self, characters: List, ideology: str, amount: float):
        """Beliefs get stronger in echo chamber"""
        if ideology not in self.chambers:
            return

        for char_id in self.chambers[ideology]:
            char = next((c for c in characters if c.id == char_id), None)
            if char:
                # Reinforce beliefs
                for belief in char.belief_system.core_beliefs:
                    char.belief_system.core_beliefs[belief] += amount
                    char.belief_system.core_beliefs[belief] = min(100,
                                                                  char.belief_system.core_beliefs[belief])

                # Reduce doubt
                char.belief_system.doubt_level *= 0.95


class Gaslighting:
    """Authority figures distort reality"""

    @staticmethod
    def distort_memory(target_char, event: str, new_interpretation: str,
                       authority_influence: float) -> bool:
        """Attempt to change someone's memory of an event"""

        # Find memories of this event
        relevant_memories = [m for m in target_char.memories
                             if event.lower() in m.event.lower()]

        if not relevant_memories:
            return False

        # Effectiveness depends on:
        # - Authority influence
        # - Target's stress (confused people easier to gaslight)
        # - Target's doubt level

        susceptibility = (
                (authority_influence / 100) * 0.4 +
                (target_char.stress / 100) * 0.3 +
                (target_char.belief_system.doubt_level / 100) * 0.3
        )

        if random.random() < susceptibility:
            # Memory altered
            for memory in relevant_memories:
                memory.interpretation = new_interpretation

            target_char.belief_system.doubt_level += 15
            return True

        return False


# ==================================================
# FILE 10: social/culture.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict, Set
import random


@dataclass
class CulturalNorm:
    """Evolving cultural norms on the ship"""
    name: str
    acceptance: float = 50.0  # 0-100, how accepted is this norm
    emerged_day: int = 0

    def normalize(self, amount: float):
        """Norm becomes more accepted"""
        self.acceptance += amount
        self.acceptance = min(100, self.acceptance)


@dataclass
class Ritual:
    """Group rituals that emerge"""
    name: str
    description: str
    participants: Set[int]
    frequency: str  # "daily", "weekly", "crisis"
    cohesion_bonus: float = 10.0
    created_day: int = 0


class CulturalEvolution:
    """How culture changes on the ship"""

    def __init__(self):
        self.norms: List[CulturalNorm] = []
        self.rituals: List[Ritual] = []
        self.taboo_words: Set[str] = set()
        self.euphemisms: Dict[str, str] = {}  # taboo -> euphemism
        self.jargon: Dict[str, str] = {}  # new word -> meaning
        self.scapegoats: List[int] = []  # character ids who are blamed

        self._init_default_norms()

    def _init_default_norms(self):
        """Initial cultural norms"""
        self.norms = [
            CulturalNorm("respecting_authority", 70.0, 0),
            CulturalNorm("helping_others", 60.0, 0),
            CulturalNorm("non_violence", 80.0, 0),
            CulturalNorm("honesty", 65.0, 0),
            CulturalNorm("equality", 50.0, 0)
        ]

    def introduce_norm(self, name: str, initial_acceptance: float, day: int):
        """New norm emerges"""
        norm = CulturalNorm(name, initial_acceptance, day)
        self.norms.append(norm)
        return norm

    def erode_norm(self, norm_name: str, amount: float):
        """Norm becomes less accepted"""
        for norm in self.norms:
            if norm.name == norm_name:
                norm.acceptance -= amount
                norm.acceptance = max(0, norm.acceptance)

                if norm.acceptance < 30:
                    print(f"    💔 Cultural norm '{norm_name}' has collapsed!")

    def create_ritual(self, name: str, description: str,
                      participants: Set[int], day: int) -> Ritual:
        """Create new ritual"""
        ritual = Ritual(
            name=name,
            description=description,
            participants=participants,
            frequency="weekly",
            created_day=day
        )
        self.rituals.append(ritual)
        return ritual

    def add_taboo_word(self, word: str, euphemism: str):
        """Word becomes taboo"""
        self.taboo_words.add(word.lower())
        self.euphemisms[word.lower()] = euphemism

    def add_jargon(self, word: str, meaning: str):
        """New terminology emerges"""
        self.jargon[word] = meaning

    def designate_scapegoat(self, char_id: int):
        """Someone becomes the scapegoat"""
        if char_id not in self.scapegoats:
            self.scapegoats.append(char_id)

    def calculate_in_group_out_group(self, characters: List) -> Dict[str, List[int]]:
        """Divide characters into in-group and out-group"""
        # Majority ideology is in-group
        ideology_counts = {}
        for char in characters:
            if char.is_alive:
                ideology = char.ideology.value
                ideology_counts[ideology] = ideology_counts.get(ideology, 0) + 1

        if not ideology_counts:
            return {"in_group": [], "out_group": []}

        majority_ideology = max(ideology_counts.items(), key=lambda x: x[1])[0]

        in_group = [c.id for c in characters
                    if c.is_alive and c.ideology.value == majority_ideology]
        out_group = [c.id for c in characters
                     if c.is_alive and c.ideology.value != majority_ideology]

        return {"in_group": in_group, "out_group": out_group}


# ==================================================
# FILE 11: power/hierarchy.py
# ==================================================

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class PowerSource(Enum):
    LEGITIMATE = "legitimate"  # Official position
    COERCIVE = "coercive"  # Force/threat
    REWARD = "reward"  # Can give benefits
    EXPERT = "expert"  # Knowledge/skill
    REFERENT = "referent"  # Charisma/respect
    INFORMATIONAL = "informational"  # Control of information


@dataclass
class PowerStructure:
    """Formal and informal power hierarchies"""

    # Official hierarchy
    official_leader: int
    officers: List[int]
    workers: List[int]

    # Actual power
    actual_power_rankings: Dict[int, float]  # char_id -> power score

    # Shadow government
    shadow_leaders: List[int] = None
    parallel_structure_exists: bool = False

    def calculate_power_score(self, char, characters: List) -> float:
        """Calculate actual power (not just official position)"""
        score = 0.0

        # Official position
        if char.id == self.official_leader:
            score += 40
        elif char.id in self.officers:
            score += 20

        # Influence
        score += char.influence * 0.3

        # Alliance power
        for alliance in [a for a in getattr(char, 'alliances_obj', [])]:
            if hasattr(alliance, 'calculate_power'):
                score += alliance.calculate_power(characters) * 0.2

        # Social network centrality
        # (would need SocialNetwork instance)

        return score

    def identify_power_vacuum(self, characters: List) -> bool:
        """Check if there's a leadership vacuum"""
        leader = next((c for c in characters if c.id == self.official_leader), None)

        if not leader or not leader.is_alive:
            return True

        if leader.influence < 30:
            return True

        # Check if shadow leaders have more power
        if self.shadow_leaders:
            for shadow_id in self.shadow_leaders:
                shadow = next((c for c in characters if c.id == shadow_id), None)
                if shadow and shadow.influence > leader.influence:
                    return True

        return False

    def power_transition(self, old_leader_id: int, new_leader_id: int):
        """Transfer of power"""
        self.official_leader = new_leader_id

        # Remove old leader from officers if they're there
        if old_leader_id in self.officers:
            self.officers.remove(old_leader_id)

    def create_parallel_structure(self, leaders: List[int]):
        """Shadow government emerges"""
        self.shadow_leaders = leaders
        self.parallel_structure_exists = True


# ==================================================
# FILE 12: power/manipulation.py
# ==================================================

from enum import Enum
from typing import List, Optional
import random


class ManipulationTactic(Enum):
    DIVIDE_AND_CONQUER = "divide_and_conquer"
    FALSE_PROMISES = "false_promises"
    SCAPEGOATING = "scapegoating"
    DISTRACTION = "distraction"
    FEAR_MONGERING = "fear_mongering"
    LOVE_BOMBING = "love_bombing"
    GASLIGHTING = "gaslighting"


class Manipulation:
    """Authority's manipulation toolkit"""

    @staticmethod
    def divide_and_conquer(authority_char, group1: List, group2: List,
                           characters: List) -> bool:
        """Pit two groups against each other"""

        # Create conflict between groups
        issue = random.choice([
            "resource distribution",
            "blame for problems",
            "cultural differences",
            "historical grievances"
        ])

        # Lower trust between groups
        for char1_id in group1:
            char1 = next((c for c in characters if c.id == char1_id), None)
            if char1:
                for char2_id in group2:
                    if char2_id in char1.trust_network:
                        char1.trust_network[char2_id] -= 20

        for char2_id in group2:
            char2 = next((c for c in characters if c.id == char2_id), None)
            if char2:
                for char1_id in group1:
                    if char1_id in char2.trust_network:
                        char2.trust_network[char1_id] -= 20

        return True

    @staticmethod
    def make_false_promises(authority_char, targets: List,
                            promise: str, characters: List) -> float:
        """Promise something with no intention to deliver"""

        belief_rate = 0.0

        for target_id in targets:
            target = next((c for c in characters if c.id == target_id), None)
            if not target:
                continue

            # Naive people believe more
            naivete = target.personality.agreeableness / 100
            trust = target.trust_network.get(authority_char.id, 50) / 100

            belief_chance = naivete * 0.5 + trust * 0.5

            if random.random() < belief_chance:
                # They believe the promise
                target.emotional_state.hope += 20
                target.stress -= 10
                belief_rate += 1
            else:
                # They see through it
                target.trust_network[authority_char.id] = max(0,
                                                              target.trust_network.get(authority_char.id, 50) - 15)
                target.emotional_state.disgust += 15

        return belief_rate / len(targets) if targets else 0

    @staticmethod
    def scapegoat_character(authority_char, scapegoat_id: int,
                            accusation: str, characters: List) -> bool:
        """Blame someone for everything"""

        scapegoat = next((c for c in characters if c.id == scapegoat_id), None)
        if not scapegoat:
            return False

        # Others turn against scapegoat
        for char in characters:
            if char.id == scapegoat_id or char.id == authority_char.id:
                continue

            # Stressed, angry people more likely to accept scapegoat
            susceptibility = (char.stress + char.emotional_state.anger) / 200

            if random.random() < susceptibility:
                char.enemies.add(scapegoat_id)
                char.trust_network[scapegoat_id] = 0
                char.emotional_state.anger -= 10  # Redirect anger

        # Scapegoat suffers
        scapegoat.stress += 30
        scapegoat.emotional_state.fear += 25
        scapegoat.emotional_state.despair += 20

        return True

    @staticmethod
    def distract_with_trivial_issue(authority_char, trivial_issue: str,
                                    characters: List):
        """Focus attention on irrelevant matter"""

        for char in characters:
            if char.id == authority_char.id:
                continue

            # Create memory of trivial issue
            char.add_memory(
                day=0,  # Would be current day
                event=f"Discussion about {trivial_issue}",
                interpretation="This seems important",
                emotional_impact=5,
                witnesses=[c.id for c in characters[:3]]
            )

            # Reduce focus on real problems
            if char.get_critical_needs():
                # They forget about critical needs temporarily
                char.stress -= 5


# ==================================================
# PART 2 COMPLETE
# ==================================================

# ==================================================
# FILE 13: morality/overton.py
# ==================================================

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class AcceptabilityLevel(Enum):
    UNTHINKABLE = "unthinkable"
    RADICAL = "radical"
    ACCEPTABLE = "acceptable"
    SENSIBLE = "sensible"
    POPULAR = "popular"
    POLICY = "policy"


@dataclass
class OvertonWindow:
    """Overton window - what's socially acceptable shifts over time"""

    behaviors: Dict[str, AcceptabilityLevel] = field(default_factory=dict)
    shift_history: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        # Initialize with default behaviors
        self.behaviors = {
            "violence": AcceptabilityLevel.UNTHINKABLE,
            "theft": AcceptabilityLevel.RADICAL,
            "lying_to_authority": AcceptabilityLevel.RADICAL,
            "hoarding_resources": AcceptabilityLevel.RADICAL,
            "public_protest": AcceptabilityLevel.ACCEPTABLE,
            "questioning_captain": AcceptabilityLevel.SENSIBLE,
            "helping_others": AcceptabilityLevel.POPULAR,
            "following_orders": AcceptabilityLevel.POLICY,
            "scapegoating": AcceptabilityLevel.UNTHINKABLE,
            "torture": AcceptabilityLevel.UNTHINKABLE,
            "cannibalism": AcceptabilityLevel.UNTHINKABLE,
            "mutiny": AcceptabilityLevel.UNTHINKABLE,
            "murder": AcceptabilityLevel.UNTHINKABLE
        }

    def shift_window(self, behavior: str, direction: int, day: int):
        """
        Shift acceptability of a behavior
        direction: +1 = more acceptable, -1 = less acceptable
        """
        if behavior not in self.behaviors:
            return

        current_level = self.behaviors[behavior]
        levels = list(AcceptabilityLevel)
        current_index = levels.index(current_level)

        new_index = max(0, min(len(levels) - 1, current_index + direction))
        new_level = levels[new_index]

        if new_level != current_level:
            self.behaviors[behavior] = new_level
            self.shift_history.append({
                'day': day,
                'behavior': behavior,
                'from': current_level.value,
                'to': new_level.value
            })

            print(f"    📊 OVERTON SHIFT: '{behavior}' is now {new_level.value}")

    def normalize_behavior(self, behavior: str, occurrences: int, day: int):
        """Repeated behavior becomes normalized"""
        # Every 3 occurrences, shift toward acceptable
        if occurrences % 3 == 0:
            self.shift_window(behavior, 1, day)

    def is_acceptable(self, behavior: str) -> bool:
        """Check if behavior is within acceptable range"""
        if behavior not in self.behaviors:
            return False

        level = self.behaviors[behavior]
        return level in [AcceptabilityLevel.ACCEPTABLE,
                         AcceptabilityLevel.SENSIBLE,
                         AcceptabilityLevel.POPULAR,
                         AcceptabilityLevel.POLICY]

    def calculate_shock_value(self, behavior: str) -> float:
        """How shocking is this behavior currently? (0-100)"""
        if behavior not in self.behaviors:
            return 50.0

        shock_map = {
            AcceptabilityLevel.UNTHINKABLE: 100.0,
            AcceptabilityLevel.RADICAL: 70.0,
            AcceptabilityLevel.ACCEPTABLE: 30.0,
            AcceptabilityLevel.SENSIBLE: 15.0,
            AcceptabilityLevel.POPULAR: 5.0,
            AcceptabilityLevel.POLICY: 0.0
        }

        return shock_map[self.behaviors[behavior]]


# ==================================================
# FILE 14: morality/ethics.py
# ==================================================

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import random


class EthicalFramework(Enum):
    DEONTOLOGICAL = "deontological"  # Rules-based
    CONSEQUENTIALIST = "consequentialist"  # Ends justify means
    VIRTUE_ETHICS = "virtue_ethics"  # Character-based
    NIHILIST = "nihilist"  # No morality


class MoralDilemmaType(Enum):
    TROLLEY_PROBLEM = "trolley_problem"
    SACRIFICE_ONE_FOR_MANY = "sacrifice_one_for_many"
    THEFT_FOR_SURVIVAL = "theft_for_survival"
    VIOLENCE_FOR_JUSTICE = "violence_for_justice"
    LYING_FOR_GOOD = "lying_for_good"


@dataclass
class MoralDilemma:
    """A moral choice characters must make"""
    dilemma_type: MoralDilemmaType
    description: str
    option_a: str
    option_b: str
    affected_characters: List[int]

    # Consequences
    option_a_consequences: Dict[str, float]
    option_b_consequences: Dict[str, float]


class EthicalSystem:
    """Tracks moral decisions and character alignment"""

    def __init__(self):
        self.moral_scores: Dict[int, float] = {}  # char_id -> morality score
        self.ethical_frameworks: Dict[int, EthicalFramework] = {}
        self.moral_history: List[Dict] = []
        self.collective_guilt: float = 0.0  # 0-100

    def initialize_character(self, char_id: int, ideology: Ideology):
        """Set initial ethical framework based on ideology"""
        framework_map = {
            Ideology.AUTHORITARIAN: EthicalFramework.DEONTOLOGICAL,
            Ideology.REVOLUTIONARY: EthicalFramework.CONSEQUENTIALIST,
            Ideology.CONSERVATIVE: EthicalFramework.VIRTUE_ETHICS,
            Ideology.LIBERAL: EthicalFramework.DEONTOLOGICAL,
            Ideology.ANARCHIST: EthicalFramework.CONSEQUENTIALIST,
            Ideology.NIHILIST: EthicalFramework.NIHILIST
        }

        self.ethical_frameworks[char_id] = framework_map.get(
            ideology, EthicalFramework.VIRTUE_ETHICS
        )
        self.moral_scores[char_id] = 50.0

    def present_dilemma(self, dilemma: MoralDilemma, character) -> str:
        """Character makes moral choice"""
        framework = self.ethical_frameworks.get(character.id,
                                                EthicalFramework.VIRTUE_ETHICS)

        # Decision based on ethical framework
        if framework == EthicalFramework.DEONTOLOGICAL:
            # Rules-based: choose based on principles
            choice = self._deontological_choice(dilemma, character)

        elif framework == EthicalFramework.CONSEQUENTIALIST:
            # Ends justify means: choose best outcome
            choice = self._consequentialist_choice(dilemma, character)

        elif framework == EthicalFramework.VIRTUE_ETHICS:
            # Character-based: what would a virtuous person do?
            choice = self._virtue_choice(dilemma, character)

        else:  # NIHILIST
            # Random or self-serving choice
            choice = random.choice(['option_a', 'option_b'])

        # Record decision
        self.moral_history.append({
            'character_id': character.id,
            'dilemma': dilemma.description,
            'choice': choice,
            'framework': framework.value
        })

        return choice

    def _deontological_choice(self, dilemma: MoralDilemma, character) -> str:
        """Rule-based decision"""
        # Prefers option that doesn't violate core rules
        if "kill" in dilemma.option_a.lower() or "harm" in dilemma.option_a.lower():
            return 'option_b'
        return 'option_a'

    def _consequentialist_choice(self, dilemma: MoralDilemma, character) -> str:
        """Outcome-based decision"""
        # Calculate net benefit of each option
        benefit_a = sum(dilemma.option_a_consequences.values())
        benefit_b = sum(dilemma.option_b_consequences.values())

        return 'option_a' if benefit_a > benefit_b else 'option_b'

    def _virtue_choice(self, dilemma: MoralDilemma, character) -> str:
        """Character-based decision"""
        # What would a person with high agreeableness do?
        if character.personality.agreeableness > 60:
            # Choose option that helps others
            return 'option_b' if "help" in dilemma.option_b.lower() else 'option_a'
        else:
            # Choose self-serving option
            return 'option_a'

    def moral_injury(self, char_id: int, severity: float):
        """Character does something against their values"""
        if char_id in self.moral_scores:
            self.moral_scores[char_id] -= severity
            self.moral_scores[char_id] = max(0, self.moral_scores[char_id])

        self.collective_guilt += severity * 0.1

    def moral_redemption(self, char_id: int, amount: float):
        """Character does something good"""
        if char_id in self.moral_scores:
            self.moral_scores[char_id] += amount
            self.moral_scores[char_id] = min(100, self.moral_scores[char_id])


# ==================================================
# FILE 15: narrative/story.py
# ==================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


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


# ==================================================
# FILE 16: narrative/memory.py
# ==================================================

from typing import List, Dict
import random


class CollectiveMemory:
    """Shared narratives and myths"""

    def __init__(self):
        self.shared_narratives: Dict[str, List[str]] = {}  # event -> interpretations
        self.dominant_narrative: Dict[str, str] = {}  # event -> accepted story
        self.myths: List[Dict] = []
        self.golden_age_myth: Optional[Dict] = None
        self.enemy_narrative: Optional[Dict] = None

    def add_event_narrative(self, event: str, narrator_id: int,
                            narrative: str, influence: float):
        """Someone tells their version of an event"""
        if event not in self.shared_narratives:
            self.shared_narratives[event] = []

        self.shared_narratives[event].append({
            'narrator': narrator_id,
            'story': narrative,
            'influence': influence,
            'believers': []
        })

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
        if days_passed % 7 == 0:
            for narrative in self.shared_narratives[event]:
                # Add distortion
                if random.random() < 0.3:
                    narrative['story'] += " [memory distorted]"


# ==================================================
# FILE 17: environment/resources.py
# ==================================================

from dataclasses import dataclass
from typing import Dict
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


print("\n" + "=" * 60)
print("SHIP OF FOOLS - COMPLETE SYSTEM (Part 3a/4)")
print("=" * 60)
print("\nAdditional Modules Created:")
print("✓ morality/overton.py - Overton Window (normalization)")
print("✓ morality/ethics.py - Ethical Systems & Moral Dilemmas")
print("✓ narrative/story.py - Story Arcs & Narrative Engine")
print("✓ narrative/memory.py - Collective Memory & Myths")
print("✓ environment/resources.py - Resource Management")
print("✓ environment/health.py - Disease & Health System")
print("\nNext (Part 3b) Will Include:")
print("- Danger/Environment system")
print("- Complete Event system")
print("- Main Ship class integration")
print("- Simulation engine")
print("\nREADY FOR PART 3b!")
print("=" * 60)