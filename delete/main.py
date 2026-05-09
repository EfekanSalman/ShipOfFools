import random
import logging
from delete.character import (
    Character, Gender, Ideology, BeliefSystem, SocialClass, HiddenAgenda, BigFive
)
from delete.social_system import SocialSystem
from delete.event_system import EventSystem

# Set up logging for better tracking of the simulation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('main_simulation').setLevel(logging.INFO)


class MainSimulation:
    def __init__(self):
        self.social_system = SocialSystem()
        self.event_system = EventSystem()
        self.turn_count = 0
        self.characters = self._create_characters()
        self._initialize_social_system()

    def _create_characters(self) -> list[Character]:
        """Creates the initial characters for the simulation."""
        logging.info("Creating characters...")

        # Defining characters with rich attributes based on the new Character class
        return [
            Character(
                name="Leo",
                gender=Gender.MALE,
                age=45,
                social_class=SocialClass.HIGH,
                ethnic_origin="Caucasian",
                sexual_orientation="heterosexual",
                ideology=Ideology.CONSERVATIVE,
                belief_system=BeliefSystem.AGNOSTICISM,
                big_five_traits={
                    BigFive.OPENNESS: 0.2, BigFive.CONSCIENTIOUSNESS: 0.9,
                    BigFive.EXTRAVERSION: 0.7, BigFive.AGREEABLENESS: 0.5,
                    BigFive.NEUROTICISM: 0.3
                },
                hidden_agenda=HiddenAgenda.SEEK_POWER,
                backstory=["Survived a major financial crisis.", "Worked in corporate management."]
            ),
            Character(
                name="Maya",
                gender=Gender.FEMALE,
                age=28,
                social_class=SocialClass.LOW,
                ethnic_origin="Hispanic",
                sexual_orientation="bisexual",
                ideology=Ideology.ANARCHIST,
                belief_system=BeliefSystem.ATHEISM,
                big_five_traits={
                    BigFive.OPENNESS: 0.8, BigFive.CONSCIENTIOUSNESS: 0.4,
                    BigFive.EXTRAVERSION: 0.6, BigFive.AGREEABLENESS: 0.2,
                    BigFive.NEUROTICISM: 0.9
                },
                hidden_agenda=HiddenAgenda.CREATE_CHAOS,
                backstory=["Witnessed social injustice.", "Lost family members in a natural disaster."]
            ),
            Character(
                name="Zoe",
                gender=Gender.FEMALE,
                age=33,
                social_class=SocialClass.MIDDLE,
                ethnic_origin="Asian",
                sexual_orientation="homosexual",
                ideology=Ideology.LIBERAL,
                belief_system=BeliefSystem.SPIRITUALITY,
                big_five_traits={
                    BigFive.OPENNESS: 0.6, BigFive.CONSCIENTIOUSNESS: 0.8,
                    BigFive.EXTRAVERSION: 0.5, BigFive.AGREEABLENESS: 0.9,
                    BigFive.NEUROTICISM: 0.4
                },
                hidden_agenda=HiddenAgenda.FIND_LOVE,
                backstory=["Grew up in a peaceful community.", "Has a strong desire for connection."]
            )
        ]

    def _initialize_social_system(self):
        """Adds characters to the social system and creates initial relationships."""
        logging.info("Initializing social system with characters...")
        for char in self.characters:
            self.social_system.add_character(char)

        # Create some initial random relationships for a starting point
        char_pairs = list(zip(self.characters, self.characters[1:] + [self.characters[0]]))
        for char1, char2 in char_pairs:
            initial_strength = random.uniform(0.3, 0.7)
            self.social_system.add_relationship(char1, char2, initial_strength)

    def _run_turn(self):
        """Runs a single turn of the simulation."""
        self.turn_count += 1
        logging.info(f"--- Turn Start: {self.turn_count} ---")

        # 1. Update character needs and psychological states
        for char in self.characters:
            char.update_needs()
            # Corrected method name: The Character class has a private method `_update_psychological_state`.
            char._update_psychological_state()
            char.make_decision()

        # 2. Characters interact and influence each other
        logging.info("Simulating character interactions...")
        for char1 in self.characters:
            for char2 in self.characters:
                if char1 != char2:
                    interaction_type = random.choice(["cooperation", "conflict"])
                    self.social_system.update_relationship(char1, char2, interaction_type)

        # 3. Trigger and apply a random event
        event = self.event_system.trigger_random_event()
        if event:
            self.event_system.apply_event_impact(self.characters, event)

        # 4. Check for and handle rebellion
        for char in self.characters:
            if char.make_decision() == "rebel":  # Use the character's decision to trigger rebellion
                leader = self.social_system.get_most_influential_character()
                if leader and leader != char:
                    logging.warning(
                        f"!!! REBELLION ALERT: {char.name} started a rebellion against leader {leader.name}!")
                    self.social_system.update_relationship(char, leader, "conflict")
                    leader.is_leader = False
                    char.is_leader = True
                    logging.info(f"{char.name} is the new leader.")
                elif not leader:
                    logging.warning(
                        f"!!! REBELLION ALERT: {char.name} started a rebellion in a leadership vacuum and became the leader.")
                    char.is_leader = True

        # 5. Log the state of characters at the end of the turn
        logging.info("--- Turn End Status Summary ---")
        for char in self.characters:
            logging.info(
                f"Character: {char.name}, Age: {char.age}, State: {char.psychological_state.value}, Health: {char.health:.2f}, "
                f"Ideology: {char.ideology.value}, Agenda: {char.hidden_agenda.value}, "
                f"Needs: {char.needs['physiological']:.2f}, Leader: {char.is_leader}")

        logging.info(f"--- Turn End: {self.turn_count} ---")
        print("\n")

    def run_simulation(self, num_turns: int):
        """Runs the entire simulation for a specified number of turns."""
        logging.info("Simulation Started!")
        leader = self.social_system.get_most_influential_character()
        if leader:
            # Note: For this to work, the Character class needs an `is_leader` attribute.
            leader.is_leader = True
            logging.info(f"Initial leader selected as {leader.name}.")

        for _ in range(num_turns):
            self._run_turn()

        logging.info("Simulation Ended.")
        self.social_system.display_relationships()


# Start the simulation
if __name__ == "__main__":
    sim = MainSimulation()
    sim.run_simulation(num_turns=10)
