"""TASK-201: a leadership institution that EMERGES from the social network,
rather than existing perfectly from tick 0 (doc 1, section 5: "do not assume
these institutions exist perfectly from the beginning. Allow them to emerge
or be created by agents.").

Mechanism: periodically, whichever agent has accumulated the most trust-
weighted influence becomes (or remains) leader — but only if that influence
clears a population-scaled threshold. Below the threshold, there simply is
no leader yet: the institution has not formed.
"""
from typing import List, Optional


class Leadership:
    def __init__(self, emergence_threshold: float = 0.15, check_interval: int = 20):
        self.leader_id: Optional[int] = None
        self.legitimacy: float = 0.0    # ground truth: avg trust the population places in the leader
        self.emergence_threshold = emergence_threshold
        self.check_interval = check_interval
        self.formed_at: Optional[int] = None

    @staticmethod
    def _influence_score(agent, social) -> float:
        """Trust others place in this agent, amplified by the agent's own
        dominance (a highly-trusted but non-assertive agent is less likely to
        step into a leadership role than an equally-trusted, dominant one)."""
        incoming = sum(edges.get(agent.id, 0.0) for edges in social.trust.values())
        return max(0.0, incoming) * (0.5 + 0.5 * agent.personality.dominance)

    def maybe_update(self, tick: int, agents: List, social):
        if tick % self.check_interval != 0:
            return
        alive = [a for a in agents if a.alive]
        if not alive:
            self.leader_id, self.legitimacy = None, 0.0
            return

        scores = {a.id: self._influence_score(a, social) for a in alive}
        best_id = max(scores, key=scores.get)
        threshold = self.emergence_threshold * len(alive)

        if scores[best_id] >= threshold:
            if self.leader_id != best_id:
                self.leader_id = best_id
                self.formed_at = tick
            trust_in_leader = [edges.get(self.leader_id, 0.0) for edges in social.trust.values()]
            self.legitimacy = max(0.0, sum(trust_in_leader) / len(trust_in_leader)) if trust_in_leader else 0.0
        else:
            # nobody has enough support: the institution has not (yet) formed
            self.leader_id = None
            self.legitimacy = 0.0
            self.formed_at = None
