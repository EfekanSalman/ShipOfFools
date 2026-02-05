"""
character.py: Defines the core Character (Agent) class and related enums.
This module encapsulates all logic and attributes pertaining to an individual agent
in the social simulation.
"""
import random
import logging
from enum import Enum
from typing import Dict, List, Any

# Configure basic logging to display info and debug messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define enums for clarity and to avoid magic strings
class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"

class Ideology(Enum):
    LIBERAL = "liberal"
    CONSERVATIVE = "conservative"
    COMMUNIST = "communist"
    ANARCHIST = "anarchist"
    NONE = "none"

class BeliefSystem(Enum):
    ATHEISM = "atheism"
    THEISM = "theism"
    SPIRITUALITY = "spirituality"
    AGNOSTICISM = "agnosticism"
    NONE = "none"

class SocialClass(Enum):
    LOW = "low"
    MIDDLE = "middle"
    HIGH = "high"

class PsychologicalState(Enum):
    NORMAL = "normal"
    ANGRY = "angry"
    DEPRESSED = "depressed"
    COOPERATIVE = "cooperative"
    PARANOID = "paranoid"

class HiddenAgenda(Enum):
    SEEK_POWER = "seek_power"
    FIND_LOVE = "find_love"
    SURVIVE = "survive"
    CREATE_CHAOS = "create_chaos"
    NONE = "none"

class BigFive(Enum):
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"

class Character:
    """
    A class representing a single agent (character) in the simulation.
    Each agent has unique traits, needs, emotions, and decision-making capabilities.
    """
    def __init__(self, name: str,
                 gender: Gender,
                 age: int,
                 social_class: SocialClass,
                 ethnic_origin: str,
                 sexual_orientation: str,
                 ideology: Ideology,
                 belief_system: BeliefSystem,
                 big_five_traits: Dict[BigFive, float],
                 hidden_agenda: HiddenAgenda = HiddenAgenda.NONE,
                 backstory: List[str] = None):
        """
        Initializes a new Character agent with a set of attributes.

        Args:
            name (str): The name of the character.
            gender (Gender): The gender identity of the character.
            age (int): The age of the character.
            social_class (SocialClass): The character's social class.
            ethnic_origin (str): The ethnic origin of the character.
            sexual_orientation (str): The sexual orientation of the character.
            ideology (Ideology): The political or social ideology.
            belief_system (BeliefSystem): The spiritual or religious belief system.
            big_five_traits (Dict[BigFive, float]): Personality traits (0.0 to 1.0).
            hidden_agenda (HiddenAgenda): A secret, guiding motivation.
            backstory (List[str]): A list of significant past events.
        """
        self.name: str = name
        self.gender: Gender = gender
        self.age: int = age
        self.social_class: SocialClass = social_class
        self.ethnic_origin: str = ethnic_origin
        self.sexual_orientation: str = sexual_orientation

        # Belief and ideology with resistance to change
        self.ideology: Ideology = ideology
        self.belief_system: BeliefSystem = belief_system
        self.resistance_to_change: Dict[str, float] = {
            "ideology": 0.5,
            "belief": 0.8,
            "prejudice": 0.2
        }

        # Personality and psychological state
        self.big_five_traits: Dict[BigFive, float] = big_five_traits
        self.needs: Dict[str, float] = {"physiological": 1.0, "social": 1.0, "psychological": 1.0}
        self.emotions: Dict[str, float] = {"anger": 0.0, "hope": 0.0, "fear": 0.0, "happiness": 0.0}
        self.psychological_state: PsychologicalState = PsychologicalState.NORMAL
        self.trauma_points: float = 0.0
        self.psychological_resilience: float = random.uniform(0.1, 1.0)

        # Hidden motivations and memory
        self.hidden_agenda: HiddenAgenda = hidden_agenda
        self.backstory: List[str] = backstory or []
        self.memory: List[Dict[str, Any]] = []

        # Physical state
        self.health: float = 1.0

    def update_needs(self) -> None:
        """
        Decreases the character's needs over time and triggers emotion changes.
        This method is a core part of the agent's behavior loop.
        """
        logging.info(f"{self.name} is updating needs...")
        # Placeholder logic: needs decrease over time
        for need in self.needs:
            self.needs[need] = max(0, self.needs[need] - 0.01)
        # Placeholder logic: affect emotions based on needs
        if self.needs["physiological"] < 0.2:
            self.emotions["anger"] = min(1.0, self.emotions["anger"] + 0.05)

        self._update_psychological_state()

    def _update_psychological_state(self):
        """
        Updates the character's psychological state based on current emotions and trauma.
        """
        if self.trauma_points > 0.8:
            self.psychological_state = PsychologicalState.PARANOID
        elif self.emotions["anger"] > 0.7 and self.needs["social"] < 0.3:
            self.psychological_state = PsychologicalState.ANGRY
        elif self.emotions["fear"] > 0.6 and self.emotions["hope"] < 0.3:
            self.psychological_state = PsychologicalState.DEPRESSED
        elif self.emotions["happiness"] > 0.7 and self.needs["social"] > 0.7:
            self.psychological_state = PsychologicalState.COOPERATIVE
        else:
            self.psychological_state = PsychologicalState.NORMAL

    def _calculate_influence(self, factor: str) -> float:
        """
        Calculates the influence of a given factor on decision-making based on personality traits.
        This is a helper method to make decision-making more dynamic.
        """
        if factor == "anger":
            # High Neuroticism increases the influence of anger
            return self.emotions["anger"] * (1 + self.big_five_traits[BigFive.NEUROTICISM])
        if factor == "cooperation":
            # High Agreeableness increases the likelihood of cooperation
            return self.big_five_traits[BigFive.AGREEABLENESS]
        if factor == "risk":
            # High Openness and low Conscientiousness might lead to risk-taking
            return self.big_five_traits[BigFive.OPENNESS] * (1 - self.big_five_traits[BigFive.CONSCIENTIOUSNESS])
        if factor == "survival":
            # Low physiological needs decrease the focus on survival
            return 1.0 - self.needs["physiological"]

        return 0.0

    def make_decision(self) -> str:
        """
        Chooses an action based on emotions, needs, personality, psychological state, and hidden agenda.
        This method will use a Strategy Pattern to select the appropriate action.
        """
        logging.info(f"{self.name} is making a decision...")
        # Determine potential actions and their influence scores
        actions: Dict[str, float] = {
            "cooperate": self._calculate_influence("cooperation"),
            "rebel": self._calculate_influence("anger"),
            "take_risk": self._calculate_influence("risk"),
            "seek_resources": self._calculate_influence("survival")
        }

        # Apply psychological state as a strong modifier
        if self.psychological_state == PsychologicalState.ANGRY:
            actions["rebel"] += 0.5
        elif self.psychological_state == PsychologicalState.DEPRESSED:
            actions["cooperate"] -= 0.3
        elif self.psychological_state == PsychologicalState.COOPERATIVE:
            actions["cooperate"] += 0.7

        # Apply hidden agenda as a strong modifier
        if self.hidden_agenda == HiddenAgenda.SEEK_POWER:
            actions["rebel"] += 0.5
            actions["cooperate"] -= 0.3
        elif self.hidden_agenda == HiddenAgenda.SURVIVE:
            actions["seek_resources"] += 0.7

        # Find the action with the highest influence score
        decision = max(actions, key=actions.get)
        return decision

    def interact_with(self, other_character: 'Character', interaction_type: str):
        """
        Simulates an interaction with another character.
        This will be used by the SocialSystem to update relationships.
        """
        # Example logic for interaction
        if interaction_type == "cooperation":
            self.emotions["happiness"] = min(1.0, self.emotions["happiness"] + 0.1 * self.big_five_traits[BigFive.AGREEABLENESS])
            other_character.emotions["happiness"] = min(1.0, other_character.emotions["happiness"] + 0.1 * other_character.big_five_traits[BigFive.AGREEABLENESS])
        elif interaction_type == "conflict":
            self.emotions["anger"] = min(1.0, self.emotions["anger"] + 0.2 * self.big_five_traits[BigFive.NEUROTICISM])
            other_character.emotions["anger"] = min(1.0, other_character.emotions["anger"] + 0.2 * other_character.big_five_traits[BigFive.NEUROTICISM])

    def change_ideology(self, event: Dict[str, Any]) -> None:
        """
        Changes the character's ideology based on an event and their resistance.
        """
        logging.info(f"{self.name} is re-evaluating their ideology due to an event.")
        # Placeholder logic for ideology change
        # A change is more likely if the character's resistance is low.
        if event.get("ideological_impact", 0) > self.resistance_to_change["ideology"]:
            logging.info(f"{self.name}'s ideology is shifting.")
            # Logic to actually change the ideology will be added here

    def perceive_event(self, event: Dict[str, Any]) -> None:
        """
        Interprets an event subjectively based on the character's biases and memory.
        This is a key part of creating conflicting realities in the simulation.
        """
        logging.info(f"{self.name} is perceiving an event.")
        # Placeholder logic for perception and memory storage
        self.memory.append({
            "event_id": event.get("id"),
            "perceived_reality": event.get("objective_info"),
            "personal_bias_applied": True
        })

    def get_memories(self) -> List[Dict[str, Any]]:
        """
        Returns the list of events stored in the character's subjective memory.
        """
        return self.memory
