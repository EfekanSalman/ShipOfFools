"""Sanity checks for the opt-in need-based decision architecture (ISSUE-014).

Run with:
    python ship_of_fools/tests/test_need_based_decision.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ship_of_fools.agents.agent import Agent
from ship_of_fools.cognition.decision import score_actions
from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


def _scores(belief=0.5, food=0.5, water=0.5, **kwargs):
    agent = Agent(0, random.Random(7))
    agent.beliefs.scarcity_belief = belief
    agent.needs.food = food
    agent.needs.water = water
    return score_actions(agent, **kwargs)


def test_need_based_scores_follow_needs_not_scarcity_belief():
    kwargs = {"need_based": True, "steal_relative_gain": 0.4}
    low_belief, high_belief = _scores(belief=0.1, **kwargs), _scores(belief=0.9, **kwargs)
    assert low_belief["steal"] == high_belief["steal"]
    assert low_belief["share"] == high_belief["share"]
    assert high_belief["forage"] < low_belief["forage"]  # believed-empty stores make foraging less attractive

    fed, hungry = _scores(food=0.9, water=0.9, **kwargs), _scores(food=0.2, water=0.2, **kwargs)
    assert hungry["steal"] > fed["steal"]
    assert hungry["share"] < fed["share"]


def test_heuristic_scores_ignore_need_based_parameters():
    assert _scores() == _scores(steal_relative_gain=0.4)


def test_hungry_agent_eats_from_wealth_only_when_need_based():
    for architecture, expect_eating in (("heuristic", False), ("need_based", True)):
        sim = Simulation(Config(n_agents=4, n_ticks=1, seed=1, decision_architecture=architecture))
        agent = sim.agents[0]
        agent.needs.food = agent.needs.water = 0.2
        agent.wealth = 5.0
        sim._update_internal_state(agent)
        if expect_eating:
            assert agent.wealth == 4.0
            assert abs(agent.needs.food - (0.2 + 0.1 - sim.config.need_decay)) < 1e-12
        else:
            assert agent.wealth == 5.0
            assert abs(agent.needs.food - (0.2 - sim.config.need_decay)) < 1e-12


def test_fed_agent_keeps_its_wealth():
    sim = Simulation(Config(n_agents=4, n_ticks=1, seed=1, decision_architecture="need_based"))
    agent = sim.agents[0]
    agent.needs.food = agent.needs.water = 0.9
    agent.wealth = 5.0
    sim._update_internal_state(agent)
    assert agent.wealth == 5.0


def test_need_based_run_is_reproducible_and_differs_from_heuristic():
    def run(architecture):
        config = Config(n_agents=16, n_ticks=40, seed=11, decision_architecture=architecture)
        return [(r["population"], r["conflict_rate"], r["avg_wealth"]) for r in Simulation(config).run().to_rows()]
    assert run("need_based") == run("need_based")
    assert run("need_based") != run("heuristic")


def test_parts_can_be_switched_separately():
    def flags(**kwargs):
        sim = Simulation(Config(n_agents=4, n_ticks=1, **kwargs))
        return sim.provisions_edible, sim.need_based_scoring
    assert flags() == (False, False)
    assert flags(decision_architecture="need_based") == (True, True)
    assert flags(provisions_edible=True) == (True, False)
    assert flags(need_based_scoring=True) == (False, True)
    assert flags(decision_architecture="need_based", provisions_edible=False) == (False, True)


def test_explicit_switches_reproduce_need_based():
    def run(**kwargs):
        config = Config(n_agents=16, n_ticks=40, seed=11, **kwargs)
        return [(r["population"], r["conflict_rate"], r["avg_wealth"]) for r in Simulation(config).run().to_rows()]
    assert run(decision_architecture="need_based") == run(provisions_edible=True, need_based_scoring=True)


def test_unknown_architecture_is_rejected():
    try:
        Simulation(Config(n_agents=4, n_ticks=1, decision_architecture="other"))
    except ValueError:
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_need_based_scores_follow_needs_not_scarcity_belief()
    test_heuristic_scores_ignore_need_based_parameters()
    test_hungry_agent_eats_from_wealth_only_when_need_based()
    test_fed_agent_keeps_its_wealth()
    test_need_based_run_is_reproducible_and_differs_from_heuristic()
    test_parts_can_be_switched_separately()
    test_explicit_switches_reproduce_need_based()
    test_unknown_architecture_is_rejected()
    print("Need-based decision checks passed.")
