from dataclasses import dataclass, field
from typing import Set, Optional
from .character import Character
from .enums import GroupIdentity

from typing import Dict

@dataclass
class Group:
    identity: GroupIdentity
    members: Dict[int, Character] = field(default_factory=dict)
    spokesperson: Optional[Character] = None

    def elect_spokesperson(self):
        if not self.members:
            self.spokesperson = None
            return

        # Elect based on speaking ability and influence
        leader = max(self.members.values(), key=lambda c: c.speaking_ability + c.influence)
        self.spokesperson = leader
        for member in self.members.values():
            member.is_spokesperson = (member.id == leader.id)

    def add_member(self, character: Character):
        self.members[character.id] = character

    def remove_member(self, character: Character):
        if character.id in self.members:
            del self.members[character.id]