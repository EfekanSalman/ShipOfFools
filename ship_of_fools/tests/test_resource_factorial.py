"""Smoke tests for the resource factorial analysis and seed assignment."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.resource_factorial import _factorial_contrasts, run_resource_factorial


def test_factorial_contrasts_known_values():
    contrasts = _factorial_contrasts({
        "C90-R0p016": 0.0,
        "C90-R0p019": 1.0,
        "C120-R0p016": 2.0,
        "C120-R0p019": 4.0,
    })
    assert contrasts["capacity_high_minus_low"] == 2.5
    assert contrasts["regen_high_minus_low"] == 1.5
    assert contrasts["capacity_by_regen_interaction"] == 1.0


def test_resource_factorial_smoke_and_disjoint_seeds():
    config = Config(n_agents=12, n_ticks=12, seed=0)
    seen_runs = []
    results = run_resource_factorial(
        config,
        n_runs=2,
        seed_start=700,
        analysis_window=6,
        bootstrap_draws=1000,
        on_run_complete=lambda cell, capacity, regen, seed, rows: seen_runs.append((cell, seed, len(rows))),
    )
    assert len(results["cells"]) == 4
    assert len(seen_runs) == 8
    assert sorted(seed for _, seed, _ in seen_runs) == list(range(700, 708))
    assert all(n_ticks == 12 for _, _, n_ticks in seen_runs)
    assert all(summary["n_seeds"] == 2 for summary in results["cell_statistics"]["cooperation_rate"].values())
    assert set(results["factorial_effects"]["conflict_rate"]) == {
        "capacity_high_minus_low", "regen_high_minus_low", "capacity_by_regen_interaction"
    }


if __name__ == "__main__":
    test_factorial_contrasts_known_values()
    test_resource_factorial_smoke_and_disjoint_seeds()
    print("Resource factorial checks passed.")
