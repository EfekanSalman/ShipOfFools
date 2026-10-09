"""Collects population-level statistics each tick (doc 1, section 12)."""
import random
import statistics

from .social_metrics import (esteban_ray_polarization, positive_adjacency,
                              in_degree_centralization, cohesion_metrics,
                              wealth_rank_persistence, NAN)


def gini(values):
    values = sorted(v for v in values if v >= 0)
    n = len(values)
    if n == 0 or sum(values) == 0:
        return 0.0
    s = sum((i + 1) * v for i, v in enumerate(values))
    return (2 * s) / (n * sum(values)) - (n + 1) / n


class MetricsTracker:
    def __init__(self, structural_interval: int = 10, mobility_window: int = 50):
        self.rows = []
        # Own, FIXED-seed RNG for metric-internal sampling (large-graph
        # clustering estimate) — never the simulation's rng, so adding or
        # removing a metric cannot perturb simulated behavior.
        self._rng = random.Random(0xA11CE)
        self.structural_interval = structural_interval
        self.mobility_window = mobility_window
        self._last_structural = {
            "belief_polarization": 0.0, "wealth_polarization": 0.0,
            "trust_centralization": 0.0, "pos_reciprocity": 0.0,
            "pos_clustering": 0.0, "giant_component_frac": 0.0,
        }
        self._last_mobility = NAN
        self._wealth_snapshot = None

    def record(self, tick, agents, social, ship, institutions=None, norms=None, lifecycle=None,
               cumulative_thieves_caught=0):
        alive = [a for a in agents if a.alive]
        if not alive:
            self.rows.append(dict(tick=tick, population=0))
            return
        wealth = [a.wealth for a in alive]

        # TASK-102/103: how wrong are agents' social models, on average?
        # Compare each stored perception of an agent's trustworthiness against a
        # ground-truth proxy (that agent's real empathy/conscientiousness) — the
        # gap is a direct measure of social misperception, not identity with it.
        gaps = []
        by_id = {a.id: a for a in alive}
        for a in alive:
            for other_id, perceived in a.mental_model.of_others.items():
                other = by_id.get(other_id)
                if other is None:
                    continue
                truth = 0.5 * (other.personality.empathy + other.personality.conscientiousness)
                gaps.append(abs(perceived.perceived_trustworthiness - truth))

        vals = [t for edges in social.trust.values() for t in edges.values()]
        positive_relationship_rate = (sum(1 for v in vals if v > 0.05) / len(vals)) if vals else 0.0
        negative_relationship_rate = (sum(1 for v in vals if v < -0.05) / len(vals)) if vals else 0.0

        # TASK-302: how much of the population has an emergent identity yet,
        # and which labels dominate.
        labels = [a.identity.label for a in alive]
        identity_formed_rate = sum(1 for l in labels if l is not None) / len(labels)
        label_rate = {
            f"identity_{name}_rate": sum(1 for l in labels if l == name) / len(labels)
            for name in ("leader", "benefactor", "opportunist", "survivor")
        }

        # Per-action shares of the living population's last action. cooperation_rate
        # and conflict_rate below are sums/aliases of these; the split shows which
        # action gained when another lost (softmax actions compete).
        action_rate = {
            f"action_{name}_rate": sum(1 for a in alive if a.last_action == name) / len(alive)
            for name in ("forage", "rest", "socialize", "share", "steal", "spread_belief")
        }

        # Structural metrics (doc 1 §12): expensive relative to the rest of this
        # function, so only recomputed every `structural_interval` ticks; other
        # ticks carry the last computed value forward (flat between updates —
        # a plotting artifact, not a claim that nothing changed mid-interval).
        alive_ids = {a.id for a in alive}
        if tick == 1 or tick % self.structural_interval == 0:
            self._last_structural["belief_polarization"] = esteban_ray_polarization(
                [a.beliefs.scarcity_belief for a in alive])
            wealth_hi = max(wealth) if wealth and max(wealth) > 0 else 1.0
            self._last_structural["wealth_polarization"] = esteban_ray_polarization(
                wealth, lo=0.0, hi=wealth_hi)
            pos_adj = positive_adjacency(social.trust, alive_ids)
            self._last_structural["trust_centralization"] = in_degree_centralization(pos_adj)
            self._last_structural.update(cohesion_metrics(pos_adj, self._rng))

        # Wealth-rank mobility: Spearman correlation of wealth rank between two
        # checkpoints `mobility_window` ticks apart (NaN until the first window
        # completes). See social_metrics.wealth_rank_persistence.
        if tick % self.mobility_window == 0:
            current_wealth = {a.id: a.wealth for a in alive}
            if self._wealth_snapshot is not None:
                self._last_mobility = wealth_rank_persistence(self._wealth_snapshot, current_wealth)
            self._wealth_snapshot = current_wealth

        self.rows.append(dict(
            tick=tick,
            population=len(alive),
            avg_stress=statistics.mean(a.stress for a in alive),
            avg_mood=statistics.mean(a.mood for a in alive),
            avg_trust=social.average_trust(),
            positive_relationship_rate=positive_relationship_rate,
            negative_relationship_rate=negative_relationship_rate,
            avg_scarcity_belief=statistics.mean(a.beliefs.scarcity_belief for a in alive),
            true_scarcity=ship.resources.true_scarcity(),
            avg_foolishness=statistics.mean(a.foolishness for a in alive),
            cooperation_rate=sum(1 for a in alive if a.last_action in ("share", "socialize")) / len(alive),
            conflict_rate=sum(1 for a in alive if a.last_action == "steal") / len(alive),
            **action_rate,
            inequality_gini=gini(wealth),
            avg_wealth=statistics.mean(wealth),
            avg_min_need=statistics.mean(min(a.needs.food, a.needs.water) for a in alive),
            # share of agents below 0.4 on food or water, the level where scarcity stress starts
            need_deficit_rate=sum(1 for a in alive if min(a.needs.food, a.needs.water) < 0.4) / len(alive),
            avg_reflected_self=statistics.mean(a.mental_model.reflected_self for a in alive),
            social_perception_gap=statistics.mean(gaps) if gaps else 0.0,
            has_leader=1 if (institutions and institutions.leader_id is not None) else 0,
            institution_legitimacy=institutions.legitimacy if institutions else 0.0,
            avg_institution_trust=statistics.mean(a.beliefs.institution_trust for a in alive),
            helping_norm=norms.helping_norm if norms else 0.5,
            authority_norm=norms.authority_norm if norms else 0.5,
            avg_health=statistics.mean(a.health for a in alive),
            identity_formed_rate=identity_formed_rate,
            **label_rate,
            avg_age=statistics.mean(a.age_years for a in alive),
            cumulative_births=lifecycle.cumulative_births if lifecycle else 0,
            cumulative_deaths_old_age=lifecycle.cumulative_deaths_old_age if lifecycle else 0,
            cumulative_deaths_starvation=lifecycle.cumulative_deaths_starvation if lifecycle else 0,
            avg_perceived_self_cooperation=statistics.mean(a.metacognition.perceived_self_cooperation for a in alive),
            avg_forage_skill=statistics.mean(a.forage_skill for a in alive),
            human_capital_total=sum(a.forage_skill for a in alive),  # skill-accumulation proxy, NOT "innovation"
            cumulative_thieves_caught=cumulative_thieves_caught,
            belief_polarization=self._last_structural["belief_polarization"],
            wealth_polarization=self._last_structural["wealth_polarization"],
            trust_centralization=self._last_structural["trust_centralization"],
            pos_reciprocity=self._last_structural["pos_reciprocity"],
            pos_clustering=self._last_structural["pos_clustering"],
            giant_component_frac=self._last_structural["giant_component_frac"],
            wealth_rank_mobility=self._last_mobility,
        ))

    def to_rows(self):
        return self.rows
