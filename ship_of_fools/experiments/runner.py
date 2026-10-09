"""Run multiple seeded simulations and compare experimental conditions
(doc 1, section 13 — "run thousands of simulations, compare distributions").
"""
import copy
import statistics

from ..simulation.engine import Simulation


def run_single(config):
    sim = Simulation(config)
    sim.run()
    return sim.metrics.to_rows()


def run_experiment(base_config, overrides: dict, n_runs: int = 10):
    """Run n_runs seeded simulations with `overrides` applied on top of base_config."""
    results = []
    for i in range(n_runs):
        cfg = copy.deepcopy(base_config)
        for k, v in overrides.items():
            setattr(cfg, k, v)
        cfg.seed = base_config.seed + i
        results.append(run_single(cfg))
    return results


def summarize_final_tick(results):
    finals = [r[-1] for r in results if r]
    if not finals:
        return {}
    keys = [k for k in finals[0].keys() if k != "tick"]
    summary = {}
    for k in keys:
        vals = [f[k] for f in finals if k in f]
        if vals:
            summary[k] = (statistics.mean(vals), statistics.pstdev(vals) if len(vals) > 1 else 0.0)
    return summary


def summarize_window(results, window: int = 50):
    """Average each run over its last `window` ticks before comparing runs —
    a single final tick is noisy (one stochastic action-selection draw per
    agent); a window smooths that out and gives experiments more power to
    separate real effects from run-to-run noise (see KNOWN_ISSUES.md ISSUE-001).
    """
    per_run_means = []
    for r in results:
        if not r:
            continue
        tail = r[-window:] if len(r) >= window else r
        keys = [k for k in tail[0].keys() if k != "tick"]
        per_run_means.append({k: statistics.mean(row[k] for row in tail if k in row) for k in keys})
    if not per_run_means:
        return {}
    keys = list(per_run_means[0].keys())
    summary = {}
    for k in keys:
        vals = [m[k] for m in per_run_means if k in m]
        if vals:
            summary[k] = (statistics.mean(vals), statistics.pstdev(vals) if len(vals) > 1 else 0.0)
    return summary
