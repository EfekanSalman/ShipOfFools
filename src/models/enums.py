from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"

class Ideology(Enum):
    AUTHORITARIAN = "authoritarian"
    REFORMIST = "reformist"
    REVOLUTIONARY = "revolutionary"
    CONSERVATIVE = "conservative"
    LIBERAL = "liberal"
    ANARCHIST = "anarchist"

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

class GroupIdentity(Enum):
    AUTHORITY = "authority"
    WORKERS = "workers"
    WOMEN = "women"
    LGBTQ = "lgbtq"
    RELIGIOUS = "religious"
    INDIGENOUS = "indigenous"
    MERCHANTS = "merchants"