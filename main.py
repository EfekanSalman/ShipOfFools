"""
main.py: The main simulation loop for the Ship of Fools project.
This script sets up the simulation environment, creates characters,
and runs the core interaction loop.
"""
import logging
import random
from typing import List
from character import (
    Character, Gender, Ideology, BeliefSystem, SocialClass, BigFive, HiddenAgenda
)
from social_system import SocialSystem, RelationshipType

# Set up logging for the main script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_characters(num_characters: int) -> List[Character]:
    """
    Creates a list of characters with randomized attributes.
    """
    characters = []
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
    genders = [Gender.MALE, Gender.FEMALE, Gender.NON_BINARY]
    ideologies = [Ideology.LIBERAL, Ideology.CONSERVATIVE, Ideology.COMMUNIST]
    social_classes = [SocialClass.LOW, SocialClass.MIDDLE, SocialClass.HIGH]
    hidden_agendas = [HiddenAgenda.SEEK_POWER, HiddenAgenda.SURVIVE, HiddenAgenda.NONE]

    for i in range(num_characters):
        name = names[i % len(names)]
        char = Character(
            name=f"{name}_{i+1}",
            gender=random.choice(genders),
            age=random.randint(20, 60),
            social_class=random.choice(social_classes),
            ethnic_origin="placeholder",
            sexual_orientation="placeholder",
            ideology=random.choice(ideologies),
            belief_system=random.choice(list(BeliefSystem)),
            big_five_traits={trait: random.uniform(0.1, 1.0) for trait in list(BigFive)},
            hidden_agenda=random.choice(hidden_agendas)
        )
        characters.append(char)
        logging.info(f"Character {char.name} created.")
    return characters

def main_simulation_loop(num_days: int):
    """
    Runs the main simulation for a specified number of days.
    """
    logging.info("Starting Ship of Fools simulation...")

    # 1. Setup the environment and characters
    characters = create_characters(5)
    social_system = SocialSystem()

    for char in characters:
        social_system.add_character(char)

    # 2. Add some initial relationships
    social_system.add_relationship(characters[0], characters[1], initial_strength=0.8, rel_type=RelationshipType.FRIENDSHIP)
    social_system.add_relationship(characters[2], characters[3], initial_strength=0.2, rel_type=RelationshipType.CONFLICT)
    social_system.add_relationship(characters[0], characters[4], initial_strength=0.5)

    # 3. Main simulation loop
    for day in range(1, num_days + 1):
        logging.info(f"--- Day {day} ---")

        # Check for a leader every 5 days
        if day % 5 == 0:
            leader = social_system.get_most_influential_character()
            if leader:
                logging.info(f"** Current leader is {leader.name}. **")

        # Each character updates their state and makes a decision
        for char in characters:
            char.update_needs()
            decision = char.make_decision()
            logging.info(f"{char.name} is feeling {char.psychological_state.value} and decided to '{decision}'.")

            # Simulate interactions based on decisions
            if decision == "cooperate":
                # Find a random character to cooperate with
                other_char = random.choice([c for c in characters if c.name != char.name])
                social_system.update_relationship(char, other_char, interaction_type="cooperation")
                char.interact_with(other_char, "cooperation")

            elif decision == "rebel":
                # Find a target to rebel against.
                leader = social_system.get_most_influential_character()
                if leader and leader.name != char.name:
                    # Rebel against the leader if the character is not the leader themselves
                    target_char = leader
                else:
                    # Otherwise, rebel against another random character
                    other_characters = [c for c in characters if c.name != char.name]
                    if other_characters:
                        target_char = random.choice(other_characters)
                    else:
                        continue # No one else to rebel against

                social_system.update_relationship(char, target_char, interaction_type="conflict")
                char.interact_with(target_char, "conflict")

        # Relationships naturally decay
        social_system.decay_relationships()

    logging.info("Simulation ended.")

if __name__ == "__main__":
    main_simulation_loop(num_days=10)
