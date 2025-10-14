from .models.character import Character, Need
from .models.group import Group
from .models.enums import GroupIdentity, Ideology
from .simulation import Simulation

def setup_simulation():
    # Create characters
    characters = [
        Character(id=1, name="Captain", role="captain", groups={GroupIdentity.AUTHORITY}, ideology=Ideology.CONSERVATIVE, needs={"power": Need("power", 90), "hunger": Need("hunger")}),
        Character(id=2, name="Worker", role="worker", groups={GroupIdentity.WORKERS}, ideology=Ideology.LIBERAL, needs={"safety": Need("safety", 40), "hunger": Need("hunger")}),
        Character(id=3, name="Spokesperson", role="spokesperson", groups={GroupIdentity.WORKERS}, ideology=Ideology.REVOLUTIONARY, needs={"respect": Need("respect", 60), "hunger": Need("hunger")}, influence=80, speaking_ability=80),
    ]

    # Create groups
    groups = {identity: Group(identity) for identity in GroupIdentity}
    for char in characters:
        for group_identity in char.groups:
            groups[group_identity].add_member(char)

    for group in groups.values():
        group.elect_spokesperson()

    return Simulation(characters, list(groups.values()))

def main():
    simulation = setup_simulation()
    simulation.run_simulation(days=10)

if __name__ == "__main__":
    main()