import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


def test_simulation_runs_and_produces_metrics():
    config = Config(n_agents=20, n_ticks=30, seed=1)
    sim = Simulation(config)
    metrics = sim.run()
    rows = metrics.to_rows()
    assert len(rows) == 30
    assert rows[-1]["population"] <= int(config.n_agents * config.max_population_multiplier)


def test_beliefs_can_diverge_from_reality():
    config = Config(n_agents=10, n_ticks=5, seed=2, perception_noise=0.5)
    sim = Simulation(config)
    sim.run()
    beliefs = [round(a.beliefs.scarcity_belief, 2) for a in sim.agents]
    assert len(set(beliefs)) > 1  # not all agents converge to an identical belief


def test_neighbor_structure_and_mental_models():
    config = Config(n_agents=24, n_ticks=60, seed=3)
    sim = Simulation(config)
    # every agent should have a nonempty local neighborhood (TASK-101)
    assert all(len(sim.social.neighbors[a]) > 0 for a in sim.agent_ids)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "social_perception_gap" in rows[-1]
    assert "avg_reflected_self" in rows[-1]
    # at least some agents should have formed a mental model of someone
    assert any(a.mental_model.of_others for a in sim.agents)


def test_institutions_can_emerge_or_stay_absent():
    # very low threshold -> some leader should emerge over a longer run
    config = Config(n_agents=30, n_ticks=200, seed=4, leadership_emergence_threshold=0.02)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "has_leader" in rows[-1]
    assert "institution_legitimacy" in rows[-1]
    assert any(r["has_leader"] == 1 for r in rows), "expected a leader to emerge at least once at this low threshold"

    # absurdly high threshold -> no one should ever qualify
    config_high = Config(n_agents=30, n_ticks=200, seed=4, leadership_emergence_threshold=999.0)
    sim_high = Simulation(config_high)
    sim_high.run()
    rows_high = sim_high.metrics.to_rows()
    assert all(r["has_leader"] == 0 for r in rows_high), "no agent should clear an impossible threshold"


def test_norms_track_cooperation_and_feed_back():
    config = Config(n_agents=40, n_ticks=150, seed=5)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "helping_norm" in rows[-1]
    # the norm should have moved away from its neutral 0.5 start at all
    assert any(abs(r["helping_norm"] - 0.5) > 0.01 for r in rows)


def test_identity_emerges_from_repeated_behavior():
    config = Config(n_agents=40, n_ticks=250, seed=6)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "identity_formed_rate" in rows[-1]
    # over 250 ticks, at least some agents should have accumulated enough
    # repeated behavior to form an identity label
    assert rows[-1]["identity_formed_rate"] > 0.0
    assert any(a.identity.label is not None for a in sim.agents)


def test_lifecycle_births_and_aging_occur():
    # favorable conditions + long horizon so births have a real chance to happen
    config = Config(n_agents=50, n_ticks=600, seed=7, birth_rate_base=0.03,
                     founder_min_age=18, founder_max_age=30)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "avg_age" in rows[-1]
    assert "population" in rows[-1]
    assert sim.lifecycle.cumulative_births > 0, "expected at least one birth over 600 favorable ticks"
    assert any(a.age_years == 0 or a.parent_ids is not None for a in sim.agents), \
        "expected at least one agent with recorded parentage"
    # ages should not all be identical to the founder seed range — aging is advancing
    ages = {a.age_years for a in sim.agents if a.alive}
    assert len(ages) > 1


def test_counterfactual_and_narrative_tools_work():
    from ship_of_fools.experiments.counterfactual import run_seeds, extinction_rate, first_divergence_tick
    from ship_of_fools.experiments.causal_narrative import extract_narrative

    config = Config(n_agents=20, n_ticks=60, seed=0)
    results = run_seeds(config, n_runs=3)
    assert len(results) == 3
    rate = extinction_rate(results, threshold=100)  # absurd threshold -> always "extinct"
    assert rate == 1.0
    rate_never = extinction_rate(results, threshold=-1)  # impossible threshold -> never
    assert rate_never == 0.0

    tick = first_divergence_tick(results[0], results[0], "true_scarcity", 0.15)
    assert tick is None  # a run compared to itself never diverges

    narrative = extract_narrative(results[0], founder_population=config.n_agents)
    assert isinstance(narrative, list)  # may be empty for a short/mild run, that's fine


def test_metacognition_and_second_order_tom():
    config = Config(n_agents=30, n_ticks=150, seed=8)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    assert "avg_perceived_self_cooperation" in rows[-1]
    # introspection should have moved at least one agent away from the neutral 0.5 start
    assert any(abs(a.metacognition.perceived_self_cooperation - 0.5) > 0.01 for a in sim.agents)
    # second-order ToM: at least one agent should have formed a per-dyad guess
    # about how a specific other agent sees them, away from the 0.5 default
    has_second_order = any(
        abs(p.they_probably_think_of_me - 0.5) > 0.01
        for a in sim.agents for p in a.mental_model.of_others.values()
    )
    assert has_second_order


def test_reconciliation_repairs_damaged_trust_faster():
    # n_agents=2 makes interaction_partner deterministic (only one possible partner)
    config = Config(n_agents=2, n_ticks=1, seed=9, neighbor_k=1)
    sim = Simulation(config)
    a, b = sim.agents[0], sim.agents[1]

    # manufacture an already-damaged relationship (as if `a` had betrayed `b` before)
    sim.social.trust[a.id][b.id] = -0.5
    before = sim.social.trust[a.id][b.id]

    sim._apply_action(a, "socialize")
    after_with_reconciliation = sim.social.trust[a.id][b.id]

    # what the SAME nudge would have produced without the reconciliation bonus
    plain_target = 0.3 + 0.4 * a.personality.empathy
    expected_plain_after = before + config.trust_learning_rate * (plain_target - before)

    assert after_with_reconciliation > expected_plain_after, \
        "reconciliation should repair a damaged relationship faster than a plain nudge"


def test_law_enforcement_and_education_and_specialization():
    from ship_of_fools.institutions.law_enforcement import LawEnforcement
    from ship_of_fools.institutions.education import apply_schooling
    import random as _random

    # law enforcement: no legitimacy -> never catches; full legitimacy -> catches often
    le = LawEnforcement(catch_probability_at_full_legitimacy=0.6)
    rng = _random.Random(1)
    assert le.maybe_catch(0.0, rng) is False
    catches = sum(1 for _ in range(200) if le.maybe_catch(1.0, rng))
    assert catches > 100  # roughly 60% of 200, allow generous margin

    # education: a child's conscientiousness/openness should rise after schooling
    config = Config(n_agents=10, n_ticks=1, seed=2)
    sim = Simulation(config)
    child = sim.agents[0]
    child.age_years = 5
    before_c, before_o = child.personality.conscientiousness, child.personality.openness
    apply_schooling(child, true_legitimacy=1.0, informal_rate=0.001,
                     institutional_rate_at_full_legitimacy=0.01)
    assert child.personality.conscientiousness >= before_c
    assert child.personality.openness >= before_o

    # specialization: forage_skill should rise after foraging
    config2 = Config(n_agents=10, n_ticks=1, seed=3)
    sim2 = Simulation(config2)
    agent = sim2.agents[0]
    assert agent.forage_skill == 0.0
    sim2._apply_action(agent, "forage")
    assert agent.forage_skill > 0.0


def test_sensitivity_screen_runs():
    from ship_of_fools.experiments.sensitivity import elementary_effects_screen, rank_by_impact

    base = Config(n_agents=20)
    baseline_mean, baseline_std, results = elementary_effects_screen(
        base, [("food_regen_rate", 0.03), ("neighbor_k", 9)], n_runs=2, n_ticks=40)
    assert "avg_trust" in baseline_mean
    assert len(results) == 2
    ranked = rank_by_impact(results)
    assert ranked[0]["impact_score"] >= ranked[1]["impact_score"]


def test_healthcare_media_and_authority_norm():
    from ship_of_fools.institutions.healthcare import health_recovery_rate
    from ship_of_fools.institutions.media import broadcast
    from ship_of_fools.culture.norms import Norms

    # healthcare: recovery rate should be higher with legitimacy than without
    no_leg = health_recovery_rate(0.0, baseline_rate=0.005, institutional_bonus_at_full_legitimacy=0.015)
    full_leg = health_recovery_rate(1.0, baseline_rate=0.005, institutional_bonus_at_full_legitimacy=0.015)
    assert full_leg > no_leg == 0.005

    # media: a broadcast with 0 legitimacy should reach no one (no crash, no-op)
    config = Config(n_agents=20, n_ticks=1, seed=10)
    sim = Simulation(config)
    leader = sim.agents[0]
    broadcast(leader, sim.agents, 0.0, config.misinformation_rate, config.confirmation_bias,
              sim.rng, tick=1, reach_fraction_at_full_legitimacy=0.5)  # should not raise

    # authority_norm: Norms.update should move it toward observed institution_trust
    norms = Norms(adapt_rate=0.5)
    norms.update(observed_cooperation_rate=0.5, observed_institution_trust=0.9)
    assert norms.authority_norm > 0.5


def test_dashboard_export_bundle_shape():
    import json
    from ship_of_fools.visualization.dashboard_export import export_bundle

    config = Config(n_agents=25, n_ticks=40, seed=11)
    bundle = json.loads(export_bundle(config, sample_size=5, snapshot_interval=10))
    assert set(bundle) == {"meta", "timeseries", "agents", "network"}
    assert len(bundle["timeseries"]) == 40
    # snapshots are taken every 10 ticks -> at most 4 per surviving sampled agent
    assert all(len(v) <= 4 for v in bundle["agents"].values())
    node_ids = {n["id"] for n in bundle["network"]["nodes"]}
    assert all(e["source"] in node_ids and e["target"] in node_ids for e in bundle["network"]["edges"])


def test_social_metrics_known_cases():
    from ship_of_fools.metrics.social_metrics import (
        esteban_ray_polarization, in_degree_centralization, cohesion_metrics,
        spearman, wealth_rank_persistence)
    import random as _random

    # polarization: identical values -> ~0; two equal masses at the extremes -> ~1
    assert esteban_ray_polarization([0.5] * 40) < 0.05
    assert esteban_ray_polarization([0.0] * 20 + [1.0] * 20) > 0.95

    # centralization: star graph (everyone points to hub 0) -> near 1;
    # a symmetric ring (each points to exactly one neighbor) -> 0 (perfectly equal in-degree)
    star = {i: ({0} if i != 0 else set()) for i in range(10)}
    assert in_degree_centralization(star) > 0.9
    n = 10
    ring = {i: {(i + 1) % n} for i in range(n)}
    assert in_degree_centralization(ring) < 0.05

    # cohesion: fully mutual triangle -> reciprocity=1, clustering=1, one component
    triangle = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    c = cohesion_metrics(triangle, _random.Random(0))
    assert abs(c["pos_reciprocity"] - 1.0) < 1e-9
    assert abs(c["pos_clustering"] - 1.0) < 1e-9
    assert abs(c["giant_component_frac"] - 1.0) < 1e-9
    # a one-directional 3-cycle (no mutual edges) -> reciprocity=0
    cycle = {0: {1}, 1: {2}, 2: {0}}
    c2 = cohesion_metrics(cycle, _random.Random(0))
    assert c2["pos_reciprocity"] == 0.0

    # spearman: identical order -> 1.0; fully reversed -> -1.0
    assert abs(spearman([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) - 1.0) < 1e-9
    assert abs(spearman([1, 2, 3, 4, 5], [50, 40, 30, 20, 10]) - (-1.0)) < 1e-9

    # wealth_rank_persistence: same ranks between snapshots -> 1.0; too few common ids -> NaN
    prev = {i: float(i) for i in range(10)}
    cur = {i: float(i) * 3 + 1 for i in range(10)}  # same relative order, different scale
    assert abs(wealth_rank_persistence(prev, cur) - 1.0) < 1e-9
    import math
    assert math.isnan(wealth_rank_persistence({0: 1.0, 1: 2.0}, {0: 1.0, 1: 2.0}))


def test_tracker_reports_structural_metrics():
    config = Config(n_agents=40, n_ticks=60, seed=12)
    sim = Simulation(config)
    sim.run()
    rows = sim.metrics.to_rows()
    last = rows[-1]
    for key in ("belief_polarization", "wealth_polarization", "trust_centralization",
                "pos_reciprocity", "pos_clustering", "giant_component_frac",
                "human_capital_total", "wealth_rank_mobility"):
        assert key in last
    assert 0.0 <= last["belief_polarization"] <= 1.0
    assert 0.0 <= last["trust_centralization"] <= 1.0


def test_statistics_module_known_cases():
    from ship_of_fools.experiments.statistics import confidence_interval, welch_t_test, cohens_d
    import random as _random

    rng = _random.Random(0)
    same_a = [rng.gauss(10, 1) for _ in range(30)]
    same_b = [rng.gauss(10, 1) for _ in range(30)]
    t, p = welch_t_test(same_a, same_b)
    assert p > 0.05, f"expected no significant difference between identical distributions, got p={p}"

    diff_a = [rng.gauss(0, 1) for _ in range(30)]
    diff_b = [rng.gauss(5, 1) for _ in range(30)]
    t2, p2 = welch_t_test(diff_a, diff_b)
    assert p2 < 0.001, f"expected a clearly significant difference, got p={p2}"
    d = cohens_d(diff_a, diff_b)
    assert abs(d) > 2.0, "a 5-SD mean shift should read as a huge effect size"

    mean, half_width, n = confidence_interval([1.0, 2.0, 3.0, 4.0, 5.0])
    assert mean == 3.0 and n == 5 and half_width > 0


def test_dashboard_export_is_strict_json():
    import json
    from ship_of_fools.visualization.dashboard_export import export_bundle

    raw = export_bundle(Config(n_agents=25, n_ticks=60, seed=3), sample_size=4)
    assert "NaN" not in raw
    def _reject(c):
        raise ValueError(f"non-standard JSON constant: {c}")
    json.loads(raw, parse_constant=_reject)  # would raise on NaN/Infinity


if __name__ == "__main__":
    test_simulation_runs_and_produces_metrics()
    test_beliefs_can_diverge_from_reality()
    test_neighbor_structure_and_mental_models()
    test_institutions_can_emerge_or_stay_absent()
    test_norms_track_cooperation_and_feed_back()
    test_identity_emerges_from_repeated_behavior()
    test_lifecycle_births_and_aging_occur()
    test_counterfactual_and_narrative_tools_work()
    test_metacognition_and_second_order_tom()
    test_reconciliation_repairs_damaged_trust_faster()
    test_law_enforcement_and_education_and_specialization()
    test_sensitivity_screen_runs()
    test_healthcare_media_and_authority_norm()
    test_dashboard_export_bundle_shape()
    test_social_metrics_known_cases()
    test_tracker_reports_structural_metrics()
    test_statistics_module_known_cases()
    test_dashboard_export_is_strict_json()
    print("All tests passed.")
