"""Systematic (screening-level) sensitivity analysis.

Full Sobol/variance-based sensitivity analysis over ~30 config parameters
would need many thousands of runs (infeasible here). Instead this implements
a Morris-style "elementary effects" screen: for each parameter, perturb it
ALONE from a shared baseline, across several seeds, and measure how much a
set of headline metrics move. This is a standard, honest first-pass
screening method — it tells you WHICH parameters matter most and roughly how
much, but (unlike full Sobol) it does not capture interaction effects between
parameters. That limitation is documented, not hidden (PROJECT_CONSTITUTION
rule 4).
"""
import copy
import statistics
from typing import Dict, List, Tuple

from ..simulation.engine import Simulation

HEADLINE_METRICS = ["avg_trust", "true_scarcity", "population", "inequality_gini",
                     "identity_formed_rate"]


def _window_mean(rows: List[dict], key: str, window: int = 50) -> float:
    tail = rows[-window:] if len(rows) >= window else rows
    vals = [r[key] for r in tail if key in r]
    return statistics.mean(vals) if vals else 0.0


def run_condition(config, n_runs: int, seed_start: int = 0, window: int = 50) -> Dict[str, float]:
    """Run n_runs seeds of `config`; return each headline metric's mean over
    the run's final `window` ticks, averaged across seeds."""
    per_run = {m: [] for m in HEADLINE_METRICS}
    for i in range(n_runs):
        cfg = copy.deepcopy(config)
        cfg.seed = seed_start + i
        sim = Simulation(cfg)
        sim.run()
        rows = sim.metrics.to_rows()
        for m in HEADLINE_METRICS:
            per_run[m].append(_window_mean(rows, m, window))
    return {m: statistics.mean(vals) for m, vals in per_run.items()}


def elementary_effects_screen(base_config, perturbations: List[Tuple[str, float]],
                               n_runs: int = 4, n_ticks: int = 300, seed_start: int = 0):
    """`perturbations` is a list of (param_name, perturbed_value). For each,
    run `n_runs` seeds at baseline and at the perturbation (same seeds, so
    per-seed noise partially cancels), and report the RAW (absolute) effect
    on each headline metric: perturbed_mean - baseline_mean, in that metric's
    own natural units.

    NOTE on normalization: an earlier version of this function normalized by
    each metric's empirical across-seed std at baseline. That breaks down
    whenever a metric is saturated at baseline (e.g. true_scarcity pinned at
    1.0, or identity_formed_rate pinned at 1.0 — both happen often in this
    model, see KNOWN_ISSUES.md), because dividing by a near-zero std produces
    meaningless, enormous numbers. Raw units are less elegant to compare
    across metrics but don't lie."""
    base_config = copy.deepcopy(base_config)
    base_config.n_ticks = n_ticks

    per_run_baseline = {m: [] for m in HEADLINE_METRICS}
    for i in range(n_runs):
        cfg = copy.deepcopy(base_config)
        cfg.seed = seed_start + i
        rows = Simulation(cfg).run().to_rows()
        for m in HEADLINE_METRICS:
            per_run_baseline[m].append(_window_mean(rows, m))
    baseline_mean = {m: statistics.mean(v) for m, v in per_run_baseline.items()}
    baseline_std = {m: (statistics.pstdev(v) if len(v) > 1 else 0.0) for m, v in per_run_baseline.items()}

    results = []
    for param, perturbed_value in perturbations:
        cfg_p = copy.deepcopy(base_config)
        setattr(cfg_p, param, perturbed_value)
        perturbed_mean = run_condition(cfg_p, n_runs, seed_start=seed_start, window=50)

        effects = {m: perturbed_mean[m] - baseline_mean[m] for m in HEADLINE_METRICS}
        results.append({"param": param, "perturbed_value": perturbed_value, "effects": effects})

    return baseline_mean, baseline_std, results


# Fixed, documented normalization scales per metric — used only for RANKING
# parameters by overall impact (not for the reported numbers themselves,
# which stay in raw units). Chosen from each metric's known/typical range,
# not from empirical baseline variance, so a saturated baseline can't break it.
RANKING_SCALE = {
    "avg_trust": 0.1,           # trust moves are meaningful in ~0.05-0.1 steps (see KNOWN_ISSUES ISSUE-002/004)
    "true_scarcity": 0.15,      # scarcity has been observed oscillating in ~0.15-0.35 bands at equilibrium
    "population": 10.0,         # a 10-agent swing is a noticeable demographic shift
    "inequality_gini": 0.05,
    "identity_formed_rate": 0.1,
}


def rank_by_impact(results: List[dict]) -> List[dict]:
    for r in results:
        r["impact_score"] = sum(abs(r["effects"][m]) / RANKING_SCALE[m] for m in HEADLINE_METRICS)
    return sorted(results, key=lambda r: -r["impact_score"])


def factorial_interaction(base_config, param_a: str, low_a: float, high_a: float,
                           param_b: str, low_b: float, high_b: float,
                           n_runs: int = 4, n_ticks: int = 300, seed_start: int = 0):
    """A 2x2 factorial design for ONE pair of parameters — the piece full
    Sobol would give you and the one-at-a-time elementary-effects screen
    above (by construction) cannot: does the effect of param_a depend on the
    level of param_b?

    Standard factorial interaction effect for metric m:
        interaction = (high_a,high_b) - (high_a,low_b) - (low_a,high_b) + (low_a,low_b)
    If |interaction| is small relative to the main effects, the two
    parameters act roughly independently (additively) over this range; if
    large, they genuinely interact and one-at-a-time screening was
    misleading about at least one of them.

    Only practical for a HANDFUL of parameter pairs (4 conditions per pair,
    each needing n_runs seeded simulations) — this is why the top-level
    screen exists to pick which pairs are worth this closer look.
    """
    conditions = {
        "low_low": {param_a: low_a, param_b: low_b},
        "low_high": {param_a: low_a, param_b: high_b},
        "high_low": {param_a: high_a, param_b: low_b},
        "high_high": {param_a: high_a, param_b: high_b},
    }
    base_config = copy.deepcopy(base_config)
    base_config.n_ticks = n_ticks

    outcomes = {}
    for name, overrides in conditions.items():
        cfg = copy.deepcopy(base_config)
        for k, v in overrides.items():
            setattr(cfg, k, v)
        outcomes[name] = run_condition(cfg, n_runs, seed_start=seed_start, window=50)

    interaction = {
        m: (outcomes["high_high"][m] - outcomes["high_low"][m]
            - outcomes["low_high"][m] + outcomes["low_low"][m])
        for m in HEADLINE_METRICS
    }
    main_effect_a = {m: (outcomes["high_high"][m] + outcomes["high_low"][m]
                          - outcomes["low_high"][m] - outcomes["low_low"][m]) / 2
                      for m in HEADLINE_METRICS}
    main_effect_b = {m: (outcomes["high_high"][m] - outcomes["high_low"][m]
                          + outcomes["low_high"][m] - outcomes["low_low"][m]) / 2
                      for m in HEADLINE_METRICS}
    return outcomes, main_effect_a, main_effect_b, interaction
