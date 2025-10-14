import unittest
from src.models.character import Character, Need
from src.models.enums import GroupIdentity, Ideology

class TestCharacter(unittest.TestCase):

    def test_character_creation(self):
        char = Character(
            id=1,
            name="Test Character",
            role="Test Role",
            groups={GroupIdentity.WORKERS},
            ideology=Ideology.LIBERAL,
            needs={"test_need": Need("test_need", 50)}
        )
        self.assertEqual(char.name, "Test Character")
        self.assertEqual(char.role, "Test Role")
        self.assertEqual(char.ideology, Ideology.LIBERAL)
        self.assertIn(GroupIdentity.WORKERS, char.groups)

    def test_update_needs(self):
        char = Character(
            id=1,
            name="Test Character",
            role="Test Role",
            groups={GroupIdentity.WORKERS},
            ideology=Ideology.LIBERAL,
            needs={"test_need": Need("test_need", 50)}
        )
        char.update_needs({"test_need": -10})
        self.assertEqual(char.needs["test_need"].value, 40)

    def test_get_critical_needs(self):
        char = Character(
            id=1,
            name="Test Character",
            role="Test Role",
            groups={GroupIdentity.WORKERS},
            ideology=Ideology.LIBERAL,
            needs={"critical_need": Need("critical_need", 20), "normal_need": Need("normal_need", 50)}
        )
        critical_needs = char.get_critical_needs()
        self.assertIn("critical_need", critical_needs)
        self.assertNotIn("normal_need", critical_needs)

if __name__ == '__main__':
    unittest.main()