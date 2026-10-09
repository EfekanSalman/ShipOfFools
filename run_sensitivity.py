"""Systematic sensitivity analysis: a Morris-style elementary-effects screen
across 19 of 53 config parameters spanning every major subsystem (cognition,
social, institutions, culture, identity, population, economy).

See ship_of_fools/experiments/sensitivity.py's docstring for the method and
its honest limitation (no interaction effects — that would need full Sobol).

Usage: python3 run_sensitivity.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.sensitivity import elementary_effects_screen, rank_by_impact, HEADLINE_METRICS


# (parameter, perturbed value) — one subsystem's worth of parameters each,
# perturbation is roughly +40-50% of baseline (or +0.15 for already-small
# [0,1] rates, capped sensibly) so every parameter gets a comparable relative nudge.
PERTURBATIONS = [
    # cognition / information
    ("perception_noise", 0.15 * 1.5),
    ("confirmation_bias", min(0.95, 0.6 + 0.15)),
    ("misinformation_rate", 0.05 + 0.15),
    # social
    ("relationship_decay", 0.004 * 1.5),
    ("trust_learning_rate", 0.15 * 1.5),
    ("neighbor_k", 9),
    ("reconciliation_bonus", 0.35 * 1.5),
    # institutions
    ("leadership_emergence_threshold", 0.012 * 1.5),
    ("tax_rate_base", 0.15 * 1.5),
    ("deterrence_strength", 0.5 * 1.5),
    # culture / identity / metacognition
    ("norm_adapt_rate", 0.03 * 1.5),
    ("identity_feedback_strength", 0.3 * 1.5),
    ("self_correction_strength", 0.3 * 1.5),
    # population
    ("birth_rate_base", 0.008 * 1.5),
    ("elderly_age", int(60 * 1.3)),
    # economy / physiology
    ("resource_capacity_per_agent", 75.0 * 1.5),
    ("food_regen_rate", 0.016 * 1.5),
    ("need_decay", 0.03 * 1.5),
    ("stress_from_scarcity_gain", 0.08 * 1.5),
]


def main():
    base = Config(n_agents=60)
    baseline_mean, baseline_std, results = elementary_effects_screen(
        base, PERTURBATIONS, n_runs=4, n_ticks=300)

    print("=== Baseline (mean ± std across seeds, last-50-tick window) ===")
    for m in HEADLINE_METRICS:
        flag = "  <-- SATURATED (std≈0): effects on this metric are ceiling-limited, read with caution" \
            if baseline_std[m] < 1e-6 else ""
        print(f"  {m:22s} {baseline_mean[m]:8.3f} ± {baseline_std[m]:.3f}{flag}")

    print("\n=== Elementary effects (raw units: perturbed_mean - baseline_mean) ===")
    print("Ranked by a fixed-scale impact score (see RANKING_SCALE in sensitivity.py) — NOT by")
    print("empirical baseline std, which breaks down for the saturated metrics flagged above.\n")
    ranked = rank_by_impact(results)
    header = f"{'parameter':30s}" + "".join(f"{m:>16s}" for m in HEADLINE_METRICS) + f"{'  impact':>10s}"
    print(header)
    for r in ranked:
        line = f"{r['param']:30s}"
        for m in HEADLINE_METRICS:
            line += f"{r['effects'][m]:16.3f}"
        line += f"{r['impact_score']:10.2f}"
        print(line)


if __name__ == "__main__":
    main()
