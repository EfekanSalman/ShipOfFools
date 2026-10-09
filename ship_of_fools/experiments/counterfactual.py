"""TASK-501: counterfactual worlds — same starting conditions, run many seeds
(doc 1, section 13: "run thousands of simulations, compare distributions"),
and optionally compare two near-identical configs seed-by-seed to see WHEN
and HOW OFTEN their trajectories diverge (doc 3, point 8's "World A vs
World B... a small initial difference -> huge societal differences").

This does not claim to prove causality from a handful of seeds — it gives a
distribution and a divergence point, which is what's honestly supportable
without a much larger compute budget.
"""
import copy
from typing import Callable, Dict, List, Optional

from ..simulation.engine import Simulation


def run_seeds(config, n_runs: int, seed_start: int = 0) -> List[List[dict]]:
    """Run n_runs independent seeds of `config`; return each run's full row list."""
    results = []
    for i in range(n_runs):
        cfg = copy.deepcopy(config)
        cfg.seed = seed_start + i
        sim = Simulation(cfg)
        sim.run()
        results.append(sim.metrics.to_rows())
    return results


def extinction_rate(results: List[List[dict]], threshold: int = 5) -> float:
    """Fraction of runs whose population fell to <= threshold by the end."""
    if not results:
        return 0.0
    ended_low = sum(1 for r in results if r and r[-1].get("population", 0) <= threshold)
    return ended_low / len(results)


def first_divergence_tick(rows_a: List[dict], rows_b: List[dict], key: str,
                           threshold: float) -> Optional[int]:
    """First tick at which two paired (same-seed-origin) runs differ in `key`
    by more than `threshold`. None if they never diverge that much."""
    for ra, rb in zip(rows_a, rows_b):
        if abs(ra.get(key, 0) - rb.get(key, 0)) > threshold:
            return ra["tick"]
    return None


def run_paired_counterfactual(base_config, overrides: Dict, n_runs: int,
                               divergence_key: str = "true_scarcity",
                               divergence_threshold: float = 0.15,
                               seed_start: int = 0):
    """Run n_runs seed-paired (world A = base_config, world B = base_config
    with `overrides`) simulations, and report the divergence tick for each pair."""
    divergence_ticks = []
    for i in range(n_runs):
        seed = seed_start + i
        cfg_a = copy.deepcopy(base_config)
        cfg_a.seed = seed
        cfg_b = copy.deepcopy(base_config)
        for k, v in overrides.items():
            setattr(cfg_b, k, v)
        cfg_b.seed = seed  # SAME seed: only the override differs

        rows_a = Simulation(cfg_a).run().to_rows()
        rows_b = Simulation(cfg_b).run().to_rows()
        tick = first_divergence_tick(rows_a, rows_b, divergence_key, divergence_threshold)
        divergence_ticks.append(tick)
    return divergence_ticks
