
# ==================================================
# FILE 21: core/ship.py (MAIN INTEGRATION)
# ==================================================
from typing import List, Optional, Set
import random

from config import CONFIG, Ideology, GroupIdentity
from core.character import Character, Need
from core.event import Event, EventGenerator
from environment.danger import DangerSystem
from environment.resources import ResourceSystem
from environment.health import HealthSystem
from morality.overton import OvertonWindow, AcceptabilityLevel
from morality.ethics import EthicalSystem
from narrative.story import NarrativeEngine
from narrative.memory import CollectiveMemory
from social.alliance import AllianceNetwork
from social.culture import CulturalEvolution
from social.communication import Propaganda, RhetoricTechnique
from social.network import SocialNetwork
from psychology.emotion import EmotionalContagion
from power.hierarchy import PowerStructure
from power.spokesperson import SpokespersonRegistry

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
        self.spokespersons: Optional[SpokespersonRegistry] = None

        # Simulation state
        self.captain_authority = 100.0
        self.social_cohesion = 70.0
        self.philosophical_tension = 30.0
        self.simulation_active = True

        # Statistics
        self.protests_held = 0
        self.mutinies_attempted = 0
        self.concessions_granted = 0
        # Philosophy-behavior temporary effects queue
        self.policy_effects: List[dict] = []
        self.last_negotiation_day: int = 0

    def initialize(self):
        """Setup initial state"""
        self._create_default_characters()
        self._setup_power_structure()
        self._initialize_character_systems()
        self.narrative_engine.auto_assign_arcs(self.characters)
        self._create_golden_age_myth()
        if CONFIG.ENABLE_SPOKESPERSONS:
            self._elect_spokespersons()

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

        # Spokesperson negotiations
        if CONFIG.ENABLE_SPOKESPERSONS and (self.day - self.last_negotiation_day) >= CONFIG.NEGOTIATION_FREQUENCY_DAYS:
            self._negotiate_with_captain()
            self.last_negotiation_day = self.day

        # Check for major events
        self._check_protests()
        self._check_mutiny()
        self._check_philosophical_crisis()
        if CONFIG.ENABLE_FRAGMENTATION:
            self._handle_power_vacuum()

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
        # Weekly memory drift on recent events
        if CONFIG.ENABLE_MEMORY_ILLUSIONS and self.event_generator.event_history and self.day % 7 == 0:
            for ev in self.event_generator.event_history[-3:]:
                self.collective_memory.distort_memory_over_time(ev.description, self.day)

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

            # Apply temporary policy/philosophy effects
            if CONFIG.ENABLE_PHILOSOPHY_EFFECTS and self.policy_effects:
                remaining_effects = []
                for eff in self.policy_effects:
                    # global effects adjust emotions/trust slightly
                    scale = CONFIG.PHILOSOPHY_EFFECT_SCALE
                    for emo, delta in eff.get('emotion_mods', {}).items():
                        char.emotional_state.modify_emotion(emo, delta * scale)
                    char.trust_in_captain += eff.get('trust_in_captain_delta', 0.0) * scale
                    eff['days_left'] -= 1
                    if eff['days_left'] > 0:
                        remaining_effects.append(eff)
                self.policy_effects = remaining_effects

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
        first_group = None
        if event.affected_groups:
            first_group = next(iter(event.affected_groups)).value
        self.collective_memory.add_event_narrative(
            event.description,
            event.instigator_id if event.instigator_id else 0,
            f"The {event.event_type.value} that changed everything",
            50.0,
            group=first_group
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

    def _elect_spokespersons(self):
        """Elect spokespersons per identity group by highest influence alive member."""
        self.spokespersons = SpokespersonRegistry()
        for group in GroupIdentity:
            candidates = [c for c in self.characters if c.is_alive and group in c.groups]
            if candidates:
                leader = max(candidates, key=lambda c: c.influence)
                self.spokespersons.set_spokesperson(group, leader.id, mandate=60.0)

    def _negotiate_with_captain(self):
        """Spokespersons present demands; outcomes affect authority and trust."""
        if not self.spokespersons:
            return
        print("\n🤝 NEGOTIATIONS WITH CAPTAIN:")
        total_impact = 0.0
        granted_needs: Set[str] = set()
        for sp in self.spokespersons.all():
            members = [c for c in self.characters if c.is_alive and sp.group in c.groups and c.role != 'captain']
            if not members:
                continue
            # Aggregate top critical needs
            needs = []
            for m in members:
                needs.extend(m.get_critical_needs())
            top = set(needs[:3]) if needs else set()
            if not top:
                continue
            # Grant a subset depending on captain authority
            grant_count = 1 if self.captain_authority < 60 else 0
            granted = set(list(top)[:grant_count])
            granted_needs |= granted
            if granted:
                for m in members:
                    for g in granted:
                        if g in m.needs:
                            m.update_needs({g: CONFIG.NEGOTIATION_BASE_EFFECT})
                total_impact += 3.0
                sp.adjust_mandate(5.0)
            else:
                # No concessions raise radicalization
                sp.adjust_radicalization(5.0)
                total_impact -= 2.0
        if granted_needs:
            print(f"  ✅ Granted: {', '.join(granted_needs)}")
        self.captain_authority = max(0.0, self.captain_authority - max(0.0, total_impact))

    def _handle_power_vacuum(self):
        """If leadership is weak, fragment into factions or transition power."""
        if not self.power_structure:
            return
        if self.captain_authority > 35:
            return
        if not self.power_structure.identify_power_vacuum(self.characters):
            return

        network = SocialNetwork(self.characters)
        clusters = [set(cl) for cl in network.find_clusters()]
        if len(clusters) >= 2:
            # Fragmentation: reduce cross-faction trust
            print("\n⚡ POWER VACUUM: SOCIETY FRAGMENTS INTO FACTIONS")
            for c in self.characters:
                for other_id in list(c.trust_network.keys()):
                    other = next((x for x in self.characters if x.id == other_id), None)
                    if not other:
                        continue
                    in_same = any(c.id in cl and other.id in cl for cl in clusters)
                    if not in_same:
                        c.trust_network[other_id] = max(0.0, c.trust_network[other_id] - CONFIG.FRAGMENTATION_TRUST_DROP)

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

        # Enqueue temporary behavior effects based on question
        if CONFIG.ENABLE_PHILOSOPHY_EFFECTS:
            effect = {'days_left': 3, 'emotion_mods': {}, 'trust_in_captain_delta': 0.0}
            if "justice" in question.lower():
                # Split between order vs equality
                effect['emotion_mods'] = {'anger': 2.0, 'trust': -1.0}
            elif "god" in question.lower():
                effect['emotion_mods'] = {'hope': 2.0, 'despair': -1.0}
            elif "meaning" in question.lower():
                effect['emotion_mods'] = {'hope': 1.5}
            self.policy_effects.append(effect)

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
