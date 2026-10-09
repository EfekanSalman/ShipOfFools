"""Sanity checks for the scarcity-belief -> action-score link ablation (ISSUE-013).

Run with:
    python ship_of_fools/tests/test_scarcity_link_ablation.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from analyze_scarcity_link_ablation import analyze
from ship_of_fools.agents.agent import Agent
from ship_of_fools.cognition.decision import score_actions
from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


def _scores_at(belief, **kwargs):
    agent = Agent(0, random.Random(7))
    agent.beliefs.scarcity_belief = belief
    return score_actions(agent, **kwargs)


def test_default_scores_read_scarcity_belief():
    low, high = _scores_at(0.1), _scores_at(0.9)
    assert high["steal"] > low["steal"]
    assert high["share"] < low["share"]


def test_ablation_arms_cut_the_direct_link_only():
    for kwargs in ({"steal_scarcity_weight": 0.0, "share_scarcity_weight": 0.0},
                   {"action_scarcity_reference": 0.5}):
        low, high = _scores_at(0.1, **kwargs), _scores_at(0.9, **kwargs)
        assert low["steal"] == high["steal"]
        assert low["share"] == high["share"]
        # spread_belief keeps its own scarcity term; the ablation does not touch it
        assert high["spread_belief"] > low["spread_belief"]


def test_fixed_reference_matches_default_at_that_belief():
    default, fixed = _scores_at(0.5), _scores_at(0.9, action_scarcity_reference=0.5)
    assert default["steal"] == fixed["steal"]
    assert default["share"] == fixed["share"]


def test_action_rates_partition_cooperation_and_conflict():
    rows = Simulation(Config(n_agents=16, n_ticks=30, seed=3)).run().to_rows()
    for row in rows:
        rates = {k: v for k, v in row.items() if k.startswith("action_")}
        assert len(rates) == 6
        assert sum(rates.values()) <= 1.0 + 1e-9  # newborns have no last action yet
        assert abs(row["cooperation_rate"] - rates["action_share_rate"] - rates["action_socialize_rate"]) < 1e-9
        assert row["conflict_rate"] == rates["action_steal_rate"]


def test_ablation_analysis_known_values():
    # capacity effect 4 in intact, 1 in zero, -2 in fixed; no regen effect
    data = {}
    for arm, effect in (("intact", 4.0), ("zero", 1.0), ("fixed", -2.0)):
        for capacity in (90.0, 120.0):
            for regen in (0.016, 0.019):
                data[(capacity, regen, arm)] = [effect * (capacity == 120.0) + seed for seed in range(5)]
    arms = analyze({"m": data}, n_draws=200)["metrics"]["m"]["arms"]
    assert arms["intact"]["contrasts"]["capacity_high_minus_low"]["estimate"] == 4.0
    assert arms["zero"]["minus_intact"]["capacity_high_minus_low"]["estimate"] == -3.0
    assert arms["zero"]["retained_fraction"]["capacity_high_minus_low"]["estimate"] == 0.25
    assert arms["fixed"]["retained_fraction"]["capacity_high_minus_low"]["estimate"] == -0.5
    assert arms["zero"]["contrasts"]["capacity_by_regen_interaction"]["estimate"] == 0.0


if __name__ == "__main__":
    test_default_scores_read_scarcity_belief()
    test_ablation_arms_cut_the_direct_link_only()
    test_fixed_reference_matches_default_at_that_belief()
    test_action_rates_partition_cooperation_and_conflict()
    test_ablation_analysis_known_values()
    print("Scarcity-link ablation checks passed.")
