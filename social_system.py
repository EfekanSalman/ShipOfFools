"""
social_system.py: Manages the social graph and relationships between characters.
This module uses the networkx library to model dynamic social interactions.
"""
import networkx as nx
import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from character import Character, BigFive

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RelationshipType(Enum):
    FRIENDSHIP = "friendship"
    CONFLICT = "conflict"
    ROMANTIC = "romantic"
    NEUTRAL = "neutral"
    ALLIANCE = "alliance"

class SocialSystem:
    """
    Manages the social relationships between characters using a graph data structure.
    """
    def __init__(self):
        """
        Initializes the social graph.
        """
        self.social_graph = nx.Graph()
        logging.info("SocialSystem initialized with an empty graph.")

    def add_character(self, character: Character):
        """
        Adds a character as a node to the social graph.
        """
        if character.name in self.social_graph:
            logging.warning(f"Character {character.name} is already in the social system.")
            return

        self.social_graph.add_node(character.name, character=character)
        logging.info(f"Character {character.name} added to the social system.")

    def add_relationship(self, character1: Character, character2: Character,
                         initial_strength: float = 0.5, rel_type: RelationshipType = RelationshipType.NEUTRAL):
        """
        Adds an initial relationship between two characters with a specified type and strength.
        The edge weight represents the relationship strength (0.0 to 1.0).
        """
        if character1.name not in self.social_graph or character2.name not in self.social_graph:
            logging.error("One or both characters are not in the social system. Cannot add relationship.")
            return

        self.social_graph.add_edge(character1.name, character2.name, weight=initial_strength, rel_type=rel_type)
        logging.info(f"Relationship ({rel_type.value}) between {character1.name} and {character2.name} added with initial strength {initial_strength:.2f}.")

    def update_relationship(self, character1: Character, character2: Character, interaction_type: str):
        """
        Updates the relationship strength and type between two characters based on a given interaction.
        """
        change = 0.0
        rel_type_change: Optional[RelationshipType] = None

        # Determine the change based on interaction type
        if interaction_type == "cooperation":
            change = 0.2
            rel_type_change = RelationshipType.FRIENDSHIP
        elif interaction_type == "conflict":
            change = -0.3
            rel_type_change = RelationshipType.CONFLICT

        if self.social_graph.has_edge(character1.name, character2.name):
            current_strength = self.social_graph[character1.name][character2.name]['weight']
            new_strength = max(0.0, min(1.0, current_strength + change))
            self.social_graph[character1.name][character2.name]['weight'] = new_strength

            current_rel_type = self.social_graph[character1.name][character2.name]['rel_type']
            if current_rel_type == RelationshipType.NEUTRAL and rel_type_change:
                self.social_graph[character1.name][character2.name]['rel_type'] = rel_type_change
                logging.info(f"Relationship type between {character1.name} and {character2.name} changed to {rel_type_change.value}.")

            logging.info(f"Relationship between {character1.name} and {character2.name} updated to {new_strength:.2f} due to '{interaction_type}'.")
        else:
            logging.warning(f"No existing relationship found between {character1.name} and {character2.name}. Adding new one.")
            self.add_relationship(character1, character2, initial_strength=max(0.0, min(1.0, change)), rel_type=rel_type_change or RelationshipType.NEUTRAL)

    def decay_relationships(self, decay_rate: float = 0.01):
        """
        Simulates the natural decay of all relationships over time.
        """
        logging.info("Decaying all relationships...")
        edges_to_remove = []
        for u, v, data in list(self.social_graph.edges(data=True)):
            current_strength = data['weight']
            new_strength = max(0, current_strength - decay_rate)
            self.social_graph[u][v]['weight'] = new_strength

            if new_strength == 0:
                edges_to_remove.append((u, v))
                logging.info(f"Relationship between {u} and {v} has decayed and been removed.")

        self.social_graph.remove_edges_from(edges_to_remove)

    def get_relationships(self, character_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Returns a dictionary of relationships for a given character, including strength and type.
        """
        if character_name not in self.social_graph:
            logging.warning(f"Character {character_name} not found in the social graph.")
            return {}

        return {neighbor: {"strength": self.social_graph[character_name][neighbor]['weight'],
                           "type": self.social_graph[character_name][neighbor]['rel_type'].value}
                for neighbor in self.social_graph.neighbors(character_name)}

    def get_most_influential_character(self) -> Optional[Character]:
        """
        Identifies the most influential character based on their social network and charisma.
        This is a simple placeholder for the leadership mechanic.
        """
        if not self.social_graph.nodes:
            logging.warning("No characters in the social system to elect a leader.")
            return None

        # Calculate influence score for each character
        influencers = {}
        for node in self.social_graph.nodes:
            char = self.social_graph.nodes[node]['character']
            # Influence is a combination of network centrality and personality trait (Extraversion)
            centrality = self.social_graph.degree(node)
            charisma_score = char.big_five_traits[BigFive.EXTRAVERSION]
            influence_score = centrality + charisma_score
            influencers[node] = influence_score

        # Find the character with the highest influence score
        leader_name = max(influencers, key=influencers.get)
        leader = self.social_graph.nodes[leader_name]['character']
        logging.info(f"Elected leader: {leader.name} with an influence score of {influencers[leader_name]:.2f}.")
        return leader
