"""Dynamic trust/relationship graph between agents.

Sparse dict-of-dicts rather than a dense matrix or networkx dependency, to
keep V0 lightweight. Swappable for a real graph library in V1+.

TASK-101: agents are NOT purely randomly paired. Each agent has a small,
stable set of "neighbors" (a Watts-Strogatz-style small-world graph — mostly
local structure, a few long-range shortcuts). Interactions are drawn mostly
from this local neighborhood, with occasional long-range contact. This is
what lets trust actually accumulate between repeat partners instead of being
diluted across the whole population every tick.
"""
import random
from typing import Dict, List, Optional, Set


def build_neighbor_structure(agent_ids: List[int], k: int, rewire_prob: float,
                              rng: random.Random) -> Dict[int, Set[int]]:
    """A ring lattice (each agent connected to its k nearest neighbors) with
    random rewiring — small-world topology, no external graph library needed."""
    n = len(agent_ids)
    neighbors: Dict[int, Set[int]] = {a: set() for a in agent_ids}
    if n < 2:
        return neighbors
    half = max(1, k // 2)
    for i, a in enumerate(agent_ids):
        for j in range(1, half + 1):
            b = agent_ids[(i + j) % n]
            neighbors[a].add(b)
            neighbors[b].add(a)
    for a in agent_ids:
        for b in list(neighbors[a]):
            if rng.random() < rewire_prob:
                candidates = [x for x in agent_ids if x != a and x not in neighbors[a]]
                if candidates:
                    new_b = rng.choice(candidates)
                    neighbors[a].discard(b)
                    neighbors[b].discard(a)
                    neighbors[a].add(new_b)
                    neighbors[new_b].add(a)
    return neighbors


class SocialNetwork:
    def __init__(self, agent_ids: List[int], rng: random.Random,
                 neighbors: Optional[Dict[int, Set[int]]] = None):
        self._rng = rng
        self.trust: Dict[int, Dict[int, float]] = {a: {} for a in agent_ids}
        self.neighbors: Dict[int, Set[int]] = neighbors or {a: set() for a in agent_ids}

    def get(self, a: int, b: int) -> float:
        return self.trust[a].get(b, 0.0)

    def nudge(self, a: int, b: int, target: float, learning_rate: float):
        cur = self.trust[a].get(b, 0.0)
        self.trust[a][b] = min(1.0, max(-1.0, cur + learning_rate * (target - cur)))

    def decay(self, rate: float):
        for edges in self.trust.values():
            for b in list(edges.keys()):
                edges[b] *= (1 - rate)

    def average_trust(self) -> float:
        vals = [t for edges in self.trust.values() for t in edges.values()]
        return sum(vals) / len(vals) if vals else 0.0

    def random_acquaintance(self, a: int, agent_ids: List[int]) -> Optional[int]:
        """O(1) expected, not O(n): reject-and-retry instead of filtering the
        whole population every call. Found via run_scale_test.py — the naive
        `[x for x in agent_ids if x != a]` made every long-range interaction
        O(n), which made the whole simulation super-linear (empirically
        n^1.26 at 1,600-10,000 agents; confirmed back to n^1.04 after this fix)."""
        if len(agent_ids) <= 1:
            return None
        for _ in range(5):  # collision (picking `a` itself) is rare; a few retries is enough
            candidate = self._rng.choice(agent_ids)
            if candidate != a:
                return candidate
        candidates = [x for x in agent_ids if x != a]  # fallback for pathological cases (tiny populations)
        return self._rng.choice(candidates) if candidates else None

    def interaction_partner(self, a: int, agent_ids: List[int],
                             long_range_prob: float = 0.15,
                             rng: Optional[random.Random] = None) -> Optional[int]:
        """Pick who agent `a` interacts with this tick: mostly a stable local
        tie, occasionally a random long-range contact (how rumors/news jump
        across otherwise-separate clusters)."""
        rng = rng or self._rng
        local = list(self.neighbors.get(a, ()))
        if local and rng.random() > long_range_prob:
            return rng.choice(local)
        if len(agent_ids) <= 1:
            return None
        for _ in range(5):
            candidate = rng.choice(agent_ids)
            if candidate != a:
                return candidate
        candidates = [x for x in agent_ids if x != a]
        return rng.choice(candidates) if candidates else None
