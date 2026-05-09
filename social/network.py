# ==================================================
# FILE 8: social/network.py
# ==================================================

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import math


class SocialNetwork:
    """Social network analysis for the ship"""

    def __init__(self, characters: List):
        self.characters = characters
        self.adjacency: Dict[int, Set[int]] = {}
        self._build_network()

    def _build_network(self):
        """Build network from character relationships"""
        for char in self.characters:
            self.adjacency[char.id] = set()

            # Add allies
            self.adjacency[char.id].update(char.alliances)

            # Add trust network connections
            for other_id, trust in char.trust_network.items():
                if trust > 50:
                    self.adjacency[char.id].add(other_id)

    def calculate_centrality(self, char_id: int) -> float:
        """Degree centrality - how connected is this character"""
        if char_id not in self.adjacency:
            return 0.0

        connections = len(self.adjacency[char_id])
        max_possible = len(self.characters) - 1

        return (connections / max_possible) * 100 if max_possible > 0 else 0

    def calculate_betweenness(self, char_id: int) -> float:
        """How often does this character bridge between groups"""
        # Simplified betweenness centrality
        bridges = 0
        total_paths = 0

        for source in self.adjacency:
            if source == char_id:
                continue
            for target in self.adjacency:
                if target == char_id or target == source:
                    continue

                total_paths += 1
                if self._is_on_path(source, target, char_id):
                    bridges += 1

        return (bridges / total_paths * 100) if total_paths > 0 else 0

    def _is_on_path(self, source: int, target: int, bridge: int) -> bool:
        """Simplified path checking"""
        return (bridge in self.adjacency.get(source, set()) and
                target in self.adjacency.get(bridge, set()))

    def find_clusters(self) -> List[Set[int]]:
        """Find densely connected groups"""
        visited = set()
        clusters = []

        for char_id in self.adjacency:
            if char_id in visited:
                continue

            cluster = self._dfs_cluster(char_id, visited)
            if len(cluster) >= 2:
                clusters.append(cluster)

        return clusters

    def _dfs_cluster(self, start: int, visited: Set[int]) -> Set[int]:
        """Depth-first search to find cluster"""
        cluster = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            cluster.add(node)

            for neighbor in self.adjacency.get(node, set()):
                if neighbor not in visited:
                    stack.append(neighbor)

        return cluster

    def calculate_network_density(self) -> float:
        """Overall network connectivity"""
        total_edges = sum(len(connections) for connections in self.adjacency.values())
        n = len(self.characters)
        max_edges = n * (n - 1)

        return (total_edges / max_edges * 100) if max_edges > 0 else 0

    def identify_influencers(self, top_n: int = 3) -> List[int]:
        """Find most influential characters by centrality"""
        centralities = [(char.id, self.calculate_centrality(char.id))
                        for char in self.characters if char.is_alive]

        centralities.sort(key=lambda x: x[1], reverse=True)
        return [char_id for char_id, _ in centralities[:top_n]]

