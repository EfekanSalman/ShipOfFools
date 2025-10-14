import unittest
from src.models.character import Character, Need
from src.models.group import Group
from src.models.enums import GroupIdentity, Ideology

class TestGroup(unittest.TestCase):

    def test_group_creation(self):
        group = Group(identity=GroupIdentity.WORKERS)
        self.assertEqual(group.identity, GroupIdentity.WORKERS)
        self.assertEqual(len(group.members), 0)

    def test_add_member(self):
        group = Group(identity=GroupIdentity.WORKERS)
        char = Character(
            id=1,
            name="Test Character",
            role="Test Role",
            groups={GroupIdentity.WORKERS},
            ideology=Ideology.LIBERAL,
            needs={"test_need": Need("test_need", 50)}
        )
        group.add_member(char)
        self.assertEqual(len(group.members), 1)

    def test_elect_spokesperson(self):
        group = Group(identity=GroupIdentity.WORKERS)
        char1 = Character(id=1, name="Char1", role="worker", groups={GroupIdentity.WORKERS}, ideology=Ideology.LIBERAL, needs={}, influence=50, speaking_ability=50)
        char2 = Character(id=2, name="Char2", role="worker", groups={GroupIdentity.WORKERS}, ideology=Ideology.LIBERAL, needs={}, influence=80, speaking_ability=80)
        group.add_member(char1)
        group.add_member(char2)
        group.elect_spokesperson()
        self.assertEqual(group.spokesperson.name, "Char2")

if __name__ == '__main__':
    unittest.main()