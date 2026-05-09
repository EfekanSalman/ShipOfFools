import random
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set
from collections import defaultdict


class Ideology(Enum):
    AUTHORITARIAN = "authoritarian"
    REFORMIST = "reformist"
    REVOLUTIONARY = "revolutionary"
    CONSERVATIVE = "conservative"
    LIBERAL = "liberal"
    ANARCHIST = "anarchist"


class GroupIdentity(Enum):
    AUTHORITY = "authority"
    WORKERS = "workers"
    WOMEN = "women"
    LGBTQ = "lgbtq"
    RELIGIOUS = "religious"
    INDIGENOUS = "indigenous"
    MERCHANTS = "merchants"


@dataclass
class Memory:
    day: int
    event: str
    interpretation: str
    emotional_impact: float
    witnesses: List[int]


@dataclass
class Need:
    name: str
    value: float  # 0-100
    critical_threshold: float = 30

    def is_critical(self) -> bool:
        return self.value < self.critical_threshold


@dataclass
class Character:
    id: int
    name: str
    role: str
    groups: Set[GroupIdentity]
    ideology: Ideology
    needs: Dict[str, Need]
    stress: float = 50.0
    trust_in_captain: float = 70.0
    memories: List[Memory] = field(default_factory=list)
    alliances: Set[int] = field(default_factory=set)
    speaking_ability: float = 50.0
    influence: float = 50.0

    def add_memory(self, day: int, event: str, interpretation: str,
                   emotional_impact: float, witnesses: List[int]):
        memory = Memory(day, event, interpretation, emotional_impact, witnesses)
        self.memories.append(memory)
        self.stress += emotional_impact * 0.5
        self.stress = min(100, max(0, self.stress))

    def recall_event(self, event_keyword: str) -> List[Memory]:
        return [m for m in self.memories if event_keyword.lower() in m.event.lower()]

    def update_needs(self, changes: Dict[str, float]):
        for need_name, change in changes.items():
            if need_name in self.needs:
                self.needs[need_name].value += change
                self.needs[need_name].value = min(100, max(0, self.needs[need_name].value))

    def get_critical_needs(self) -> List[str]:
        return [name for name, need in self.needs.items() if need.is_critical()]

    def calculate_satisfaction(self) -> float:
        if not self.needs:
            return 50.0
        return sum(need.value for need in self.needs.values()) / len(self.needs)


class PhilosophicalQuestion:
    def __init__(self, question: str, perspectives: Dict[Ideology, str]):
        self.question = question
        self.perspectives = perspectives

    def get_perspective(self, ideology: Ideology) -> str:
        return self.perspectives.get(ideology, "No clear answer")


@dataclass
class Event:
    day: int
    type: str
    description: str
    affected_groups: Set[GroupIdentity]
    impact: Dict[str, float]


class Alliance:
    def __init__(self, members: Set[int], purpose: str, strength: float = 50.0):
        self.members = members
        self.purpose = purpose
        self.strength = strength
        self.created_day = 0
        self.broken = False

    def add_member(self, char_id: int):
        self.members.add(char_id)
        self.strength += 5

    def remove_member(self, char_id: int):
        self.members.discard(char_id)
        self.strength -= 10
        if len(self.members) < 2:
            self.broken = True


class Ship:
    def __init__(self):
        self.day = 1
        self.temperature = 15  # Celsius
        self.heading = 0  # 0 = North (danger), 180 = South (safety)
        self.danger_level = 0  # 0-100
        self.captain_authority = 100
        self.social_cohesion = 70
        self.philosophical_tension = 30
        self.characters: List[Character] = []
        self.events: List[Event] = []
        self.alliances: List[Alliance] = []
        self.narratives: Dict[int, str] = {}  # char_id -> their version of reality
        self.philosophical_questions = self._init_philosophical_questions()

    def _init_philosophical_questions(self) -> List[PhilosophicalQuestion]:
        return [
            PhilosophicalQuestion(
                "What is the meaning of this voyage?",
                {
                    Ideology.AUTHORITARIAN: "To maintain order and hierarchy",
                    Ideology.REVOLUTIONARY: "To overthrow oppressive structures",
                    Ideology.CONSERVATIVE: "To preserve traditional values",
                    Ideology.LIBERAL: "To ensure everyone's rights are protected",
                    Ideology.ANARCHIST: "To abolish all authority"
                }
            ),
            PhilosophicalQuestion(
                "Is God punishing us?",
                {
                    Ideology.CONSERVATIVE: "Yes, for abandoning traditional values",
                    Ideology.LIBERAL: "God doesn't interfere in human affairs",
                    Ideology.REVOLUTIONARY: "There is no God, only human struggle",
                    Ideology.AUTHORITARIAN: "God supports legitimate authority"
                }
            ),
            PhilosophicalQuestion(
                "What is justice?",
                {
                    Ideology.AUTHORITARIAN: "Justice is order and discipline",
                    Ideology.REVOLUTIONARY: "Justice is equality and liberation",
                    Ideology.REFORMIST: "Justice is gradual improvement",
                    Ideology.LIBERAL: "Justice is protecting individual rights"
                }
            )
        ]

    def add_character(self, character: Character):
        self.characters.append(character)

    def create_default_characters(self):
        chars = [
            Character(1, "Captain", "captain", {GroupIdentity.AUTHORITY},
                      Ideology.AUTHORITARIAN,
                      {"power": Need("power", 90), "respect": Need("respect", 80)},
                      stress=20, influence=90, speaking_ability=80),

            Character(2, "Third Officer", "officer", {GroupIdentity.AUTHORITY},
                      Ideology.LIBERAL,
                      {"power": Need("power", 70), "manipulation": Need("manipulation", 80)},
                      stress=15, influence=70, speaking_ability=85),

            Character(3, "English Sailor", "worker", {GroupIdentity.WORKERS},
                      Ideology.REFORMIST,
                      {"wage": Need("wage", 40), "safety": Need("safety", 50),
                       "warmth": Need("warmth", 45)},
                      stress=60, influence=40, speaking_ability=50),

            Character(4, "Mexican Sailor", "worker", {GroupIdentity.WORKERS, GroupIdentity.INDIGENOUS},
                      Ideology.REVOLUTIONARY,
                      {"wage": Need("wage", 25), "equality": Need("equality", 20),
                       "language_rights": Need("language_rights", 30)},
                      stress=70, influence=35, speaking_ability=45),

            Character(5, "Woman Passenger", "passenger", {GroupIdentity.WOMEN},
                      Ideology.LIBERAL,
                      {"warmth": Need("warmth", 30), "equality": Need("equality", 40),
                       "safety": Need("safety", 60)},
                      stress=65, influence=45, speaking_ability=60),

            Character(6, "Native Sailor", "worker", {GroupIdentity.INDIGENOUS, GroupIdentity.WORKERS},
                      Ideology.REVOLUTIONARY,
                      {"reparations": Need("reparations", 10), "autonomy": Need("autonomy", 20),
                       "wage": Need("wage", 35)},
                      stress=75, influence=30, speaking_ability=40),

            Character(7, "Boatswain (Lostromo)", "worker", {GroupIdentity.LGBTQ, GroupIdentity.WORKERS},
                      Ideology.LIBERAL,
                      {"dignity": Need("dignity", 40), "acceptance": Need("acceptance", 35),
                       "wage": Need("wage", 45)},
                      stress=68, influence=38, speaking_ability=55),

            Character(8, "Animal Rights Activist", "passenger", {GroupIdentity.RELIGIOUS},
                      Ideology.LIBERAL,
                      {"animal_welfare": Need("animal_welfare", 25), "morality": Need("morality", 50)},
                      stress=72, influence=25, speaking_ability=65),

            Character(9, "Professor", "intellectual", {GroupIdentity.AUTHORITY},
                      Ideology.REVOLUTIONARY,
                      {"justice": Need("justice", 30), "revolution": Need("revolution", 40)},
                      stress=55, influence=60, speaking_ability=90),

            Character(10, "Steward", "worker", {GroupIdentity.WORKERS},
                      Ideology.ANARCHIST,
                      {"survival": Need("survival", 70), "truth": Need("truth", 60)},
                      stress=80, influence=20, speaking_ability=70),
        ]

        for char in chars:
            self.add_character(char)

    def calculate_danger(self):
        # Danger increases as ship goes north
        self.danger_level = (360 - self.heading) / 360 * 100
        self.temperature = 15 - (self.danger_level / 100) * 20

    def simulate_day(self):
        print(f"\n{'=' * 60}")
        print(f"DAY {self.day}")
        print(f"{'=' * 60}")
        print(f"Ship Heading: {self.heading}° (0=North/Danger, 180=South/Safety)")
        print(f"Temperature: {self.temperature:.1f}°C")
        print(f"Danger Level: {self.danger_level:.1f}/100")
        print(f"Captain Authority: {self.captain_authority:.1f}/100")
        print(f"Social Cohesion: {self.social_cohesion:.1f}/100")
        print(f"Philosophical Tension: {self.philosophical_tension:.1f}/100")

        # Ship continues north
        self.heading = max(0, self.heading - 2)
        self.calculate_danger()

        # Environmental effects
        self._apply_environmental_effects()

        # Generate events
        self._generate_daily_events()

        # Character interactions
        self._character_interactions()

        # Alliance dynamics
        self._update_alliances()

        # Philosophical discussions
        if random.random() < 0.3:
            self._philosophical_discussion()

        # Protests
        if self._check_protest_conditions():
            self._organize_protest()

        # Check for mutiny
        if self._check_mutiny_conditions():
            self._attempt_mutiny()

        # Check for ship sinking
        if self.danger_level > 90 and random.random() < 0.3:
            self._ship_sinks()
            return False

        self.day += 1
        return True

    def _apply_environmental_effects(self):
        for char in self.characters:
            if "warmth" in char.needs:
                char.update_needs({"warmth": -(self.danger_level / 20)})

            if "safety" in char.needs:
                char.update_needs({"safety": -(self.danger_level / 30)})

            char.stress += self.danger_level / 40

    def _generate_daily_events(self):
        events = []

        # Random incidents
        if random.random() < 0.2:
            incident_type = random.choice(["theft", "fight", "accident", "dog_abuse"])
            events.append(self._create_incident(incident_type))

        # Resource scarcity
        if self.temperature < 5 and random.random() < 0.4:
            events.append(self._create_scarcity_event())

        for event in events:
            self._process_event(event)

    def _create_incident(self, incident_type: str) -> Event:
        if incident_type == "theft":
            return Event(
                self.day, "theft",
                "Someone stole food from the kitchen",
                {GroupIdentity.WORKERS, GroupIdentity.AUTHORITY},
                {"trust": -5, "tension": 10}
            )
        elif incident_type == "fight":
            return Event(
                self.day, "fight",
                "A fight broke out between crew members",
                {GroupIdentity.WORKERS},
                {"cohesion": -8, "stress": 5}
            )
        elif incident_type == "dog_abuse":
            return Event(
                self.day, "dog_abuse",
                "The dog was kicked by an officer",
                {GroupIdentity.RELIGIOUS, GroupIdentity.AUTHORITY},
                {"morality": -10, "tension": 8}
            )
        else:
            return Event(
                self.day, "accident",
                "A worker was injured on deck",
                {GroupIdentity.WORKERS},
                {"safety": -10, "stress": 8}
            )

    def _create_scarcity_event(self) -> Event:
        return Event(
            self.day, "scarcity",
            "Blankets are running out due to extreme cold",
            {GroupIdentity.WOMEN, GroupIdentity.WORKERS},
            {"warmth": -15, "tension": 12}
        )

    def _process_event(self, event: Event):
        print(f"\n🔔 EVENT: {event.description}")
        self.events.append(event)

        # Different characters remember differently
        for char in self.characters:
            if any(g in event.affected_groups for g in char.groups):
                interpretation = self._generate_interpretation(char, event)
                witnesses = [c.id for c in self.characters if random.random() < 0.6]
                char.add_memory(self.day, event.description, interpretation,
                                abs(sum(event.impact.values())), witnesses)
                print(f"  {char.name}'s view: {interpretation}")

    def _generate_interpretation(self, char: Character, event: Event) -> str:
        interpretations = {
            Ideology.AUTHORITARIAN: f"This disrupts order. Authority must be maintained.",
            Ideology.REVOLUTIONARY: f"This is systemic oppression. We must resist!",
            Ideology.LIBERAL: f"This violates individual rights. We need reform.",
            Ideology.CONSERVATIVE: f"This shows moral decay. Return to tradition.",
            Ideology.REFORMIST: f"This shows we need gradual improvements.",
            Ideology.ANARCHIST: f"This proves all hierarchy is corrupt."
        }
        return interpretations.get(char.ideology, "This is concerning.")

    def _character_interactions(self):
        # Characters form or break alliances
        for char in self.characters:
            if random.random() < 0.15:
                potential_ally = self._find_potential_ally(char)
                if potential_ally:
                    self._form_alliance(char, potential_ally)

    def _find_potential_ally(self, char: Character) -> Character:
        candidates = []
        for other in self.characters:
            if other.id != char.id and other.id not in char.alliances:
                # Check ideological similarity
                if char.ideology == other.ideology:
                    candidates.append(other)
                # Check shared groups
                elif char.groups & other.groups:
                    candidates.append(other)

        return random.choice(candidates) if candidates else None

    def _form_alliance(self, char1: Character, char2: Character):
        char1.alliances.add(char2.id)
        char2.alliances.add(char1.id)

        # Check if alliance already exists
        for alliance in self.alliances:
            if char1.id in alliance.members or char2.id in alliance.members:
                alliance.add_member(char1.id)
                alliance.add_member(char2.id)
                print(f"  🤝 {char1.name} and {char2.name} joined existing alliance")
                return

        # Create new alliance
        purpose = f"Shared {random.choice(['ideology', 'identity', 'grievances'])}"
        new_alliance = Alliance({char1.id, char2.id}, purpose)
        new_alliance.created_day = self.day
        self.alliances.append(new_alliance)
        print(f"  🤝 NEW ALLIANCE: {char1.name} & {char2.name} ({purpose})")

    def _update_alliances(self):
        for alliance in self.alliances:
            if alliance.broken:
                continue

            # Alliances can strengthen or weaken
            if random.random() < 0.1:
                alliance.strength += random.uniform(-5, 5)

                if alliance.strength < 20:
                    print(f"  💔 Alliance broke apart ({alliance.purpose})")
                    alliance.broken = True

    def _philosophical_discussion(self):
        question = random.choice(self.philosophical_questions)
        print(f"\n💭 PHILOSOPHICAL DISCUSSION: '{question.question}'")

        speakers = random.sample([c for c in self.characters if c.speaking_ability > 40],
                                 min(3, len(self.characters)))

        for speaker in speakers:
            perspective = question.get_perspective(speaker.ideology)
            print(f"  {speaker.name}: {perspective}")
            speaker.influence += 2

        self.philosophical_tension += random.uniform(5, 15)

    def _check_protest_conditions(self) -> bool:
        critical_needs_count = sum(
            1 for char in self.characters
            if char.get_critical_needs() and char.role != "captain"
        )

        avg_stress = sum(c.stress for c in self.characters) / len(self.characters)

        return critical_needs_count >= 3 and avg_stress > 60

    def _organize_protest(self):
        protesters = [c for c in self.characters
                      if c.role != "captain" and c.get_critical_needs()]

        if not protesters:
            return

        print(f"\n⚠️ PROTEST ORGANIZED!")
        print(f"  Protesters: {', '.join(p.name for p in protesters)}")

        demands = set()
        for protester in protesters:
            critical = protester.get_critical_needs()
            demands.update(critical)
            print(f"  {protester.name} demands: {', '.join(critical)}")

        # Officer intervenes
        officer = next((c for c in self.characters if c.role == "officer"), None)
        if officer:
            print(f"  {officer.name}: 'I understand your concerns. Keep protesting peacefully.'")

        # Captain makes concessions
        concessions = self._captain_makes_concessions(demands, protesters)

        if concessions:
            print(f"  ✅ Captain grants: {', '.join(concessions)}")
            self.captain_authority -= 5

            for protester in protesters:
                for concession in concessions:
                    if concession in protester.needs:
                        protester.update_needs({concession: 10})
                protester.stress -= 5

        # But ship still heads north
        print(f"  ⚠️ However, the ship continues north...")

        # Steward's warning
        steward = next((c for c in self.characters if "steward" in c.name.lower()), None)
        if steward:
            print(f"\n  {steward.name}: 'We need to turn the ship south! These concessions")
            print(f"  mean nothing if we all drown!'")
            print(f"  Others: 'Fascist! Counter-revolutionary!'")
            steward.stress += 10
            steward.influence -= 5

    def _captain_makes_concessions(self, demands: Set[str], protesters: List[Character]) -> List[str]:
        # Captain grants some but not all demands
        concession_count = min(len(demands), random.randint(1, 3))
        return random.sample(list(demands), concession_count)

    def _check_mutiny_conditions(self) -> bool:
        if self.captain_authority > 40:
            return False

        revolutionary_count = sum(
            1 for c in self.characters
            if c.ideology in [Ideology.REVOLUTIONARY, Ideology.ANARCHIST]
            and c.stress > 70
        )

        return revolutionary_count >= 3 and self.danger_level > 60

    def _attempt_mutiny(self):
        mutineers = [c for c in self.characters
                     if c.ideology in [Ideology.REVOLUTIONARY, Ideology.ANARCHIST]
                     and c.role != "captain"]

        print(f"\n🔥 MUTINY ATTEMPT!")
        print(f"  Mutineers: {', '.join(m.name for m in mutineers)}")

        # Check if they have support
        support_count = sum(1 for c in self.characters
                            if c.trust_in_captain < 30 and c.role != "captain")

        if support_count > len(self.characters) / 2:
            print(f"  ✅ MUTINY SUCCEEDS! Captain is overthrown!")
            self.captain_authority = 0

            # New leadership emerges
            new_leader = max(mutineers, key=lambda c: c.influence)
            print(f"  👑 {new_leader.name} becomes the new leader!")
            print(f"  🔄 Ship turns south!")
            self.heading = 180

        else:
            print(f"  ❌ MUTINY FAILS! Not enough support.")
            print(f"  Professor: 'I don't believe in violence!'")
            for mutineer in mutineers:
                mutineer.stress += 15
                mutineer.influence -= 10

    def _ship_sinks(self):
        print(f"\n{'=' * 60}")
        print(f"💀 THE SHIP HITS ICEBERGS AND SINKS!")
        print(f"{'=' * 60}")
        print(f"\nEveryone drowns.")
        print(f"\nThe ship traveled {360 - self.heading}° north into danger.")
        print(f"While passengers argued about:")

        all_demands = set()
        for char in self.characters:
            all_demands.update(char.get_critical_needs())

        for demand in all_demands:
            print(f"  - {demand}")

        print(f"\n...nobody listened to the steward's warning to turn south.")
        print(f"\nFinal Statistics:")
        print(f"  Days survived: {self.day}")
        print(f"  Protests held: {len([e for e in self.events if 'protest' in e.type.lower()])}")
        print(f"  Captain's final authority: {self.captain_authority:.1f}/100")
        print(f"  Average stress level: {sum(c.stress for c in self.characters) / len(self.characters):.1f}/100")

    def print_status(self):
        print(f"\n📊 CHARACTER STATUS:")
        for char in self.characters:
            satisfaction = char.calculate_satisfaction()
            print(f"\n  {char.name} ({char.role})")
            print(f"    Groups: {', '.join(g.value for g in char.groups)}")
            print(f"    Ideology: {char.ideology.value}")
            print(f"    Satisfaction: {satisfaction:.1f}/100")
            print(f"    Stress: {char.stress:.1f}/100")
            print(f"    Trust in Captain: {char.trust_in_captain:.1f}/100")
            print(f"    Influence: {char.influence:.1f}/100")

            critical = char.get_critical_needs()
            if critical:
                print(f"    ⚠️ Critical needs: {', '.join(critical)}")

            if char.alliances:
                print(f"    Allies: {len(char.alliances)}")

        print(f"\n🤝 ACTIVE ALLIANCES: {len([a for a in self.alliances if not a.broken])}")
        for i, alliance in enumerate([a for a in self.alliances if not a.broken]):
            members = [c.name for c in self.characters if c.id in alliance.members]
            print(f"  Alliance {i + 1}: {', '.join(members)}")
            print(f"    Purpose: {alliance.purpose}")
            print(f"    Strength: {alliance.strength:.1f}/100")


def main():
    ship = Ship()
    ship.create_default_characters()

    print("🚢 SHIP OF FOOLS - SOCIAL SIMULATION")
    print("Based on Theodore Kaczynski's allegory")
    print("\nThe ship heads north into dangerous waters...")
    print("Will anyone listen to reason before it's too late?")

    # Run simulation
    days_to_simulate = 30

    for _ in range(days_to_simulate):
        if not ship.simulate_day():
            break  # Ship sank

        if ship.day % 5 == 0:
            ship.print_status()

        # Small delay for readability
        input("\nPress Enter to continue to next day...")

    print("\n\n📖 SIMULATION COMPLETE")
    print("\nThis simulation demonstrates how:")
    print("- Groups focus on immediate grievances while ignoring existential threats")
    print("- Authority manipulates through small concessions")
    print("- Those warning about real danger are dismissed as extremists")
    print("- Conflicting memories and narratives prevent unified action")
    print("- The ship sinks while everyone argues about distribution of deck chairs")


if __name__ == "__main__":
    main()