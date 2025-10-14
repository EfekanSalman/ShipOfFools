from typing import List, Optional
from ..models.character import Character
from ..models.group import Group

class LeadershipSystem:
    def __init__(self, characters: List[Character], groups: List[Group]):
        self.characters = characters
        self.groups = groups
        self.captain: Optional[Character] = self.get_captain()

    def get_captain(self) -> Optional[Character]:
        for char in self.characters:
            if char.role == "captain":
                return char
        return None

    def update_captain_authority(self, change: float):
        if self.captain:
            self.captain.trust_in_captain += change

    def check_for_leadership_change(self):
        if self.captain and self.captain.trust_in_captain < 40:
            print("\n🚨 CAPTAIN'S AUTHORITY IS WEAK! A new leader may emerge...")

            candidates = [g.spokesperson for g in self.groups if g.spokesperson and g.spokesperson.id != self.captain.id]

            if not candidates:
                print("  No spokespersons to challenge the captain.")
                return

            power_scores = {char: char.influence for char in candidates}

            if not power_scores:
                print("  No candidates have influence.")
                return

            new_leader = max(power_scores, key=power_scores.get)

            if new_leader.influence > self.captain.influence + self.captain.trust_in_captain:
                print(f"  {self.captain.name} has been deposed!")
                self.captain.role = "deposed"
                new_leader.role = "captain"
                self.captain = new_leader
                print(f"  👑 {new_leader.name} has become the new Captain!")
            else:
                print("  No single leader is strong enough to take over yet.")