# ==================================================

# FILE 1: config.py
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

    # Feature flags
    ENABLE_MEMORY_ILLUSIONS: bool = True
    ENABLE_SPOKESPERSONS: bool = True
    ENABLE_PHILOSOPHY_EFFECTS: bool = True
    ENABLE_FRAGMENTATION: bool = True

    # Tuning knobs
    MEMORY_DRIFT_RATE: float = 0.3  # weekly drift strength (0-1)
    MEMORY_BIAS_INTENSITY: float = 0.6  # per-character perception bias (0-1)
    NEGOTIATION_FREQUENCY_DAYS: int = 3  # days between spokesperson negotiations
    NEGOTIATION_BASE_EFFECT: float = 5.0  # base satisfaction delta per granted demand
    PHILOSOPHY_EFFECT_SCALE: float = 0.6  # scales emotion/trust modifiers from discussions
    FRAGMENTATION_TRUST_DROP: float = 10.0  # trust drop between factions on fragmentation


CONFIG = Config()
