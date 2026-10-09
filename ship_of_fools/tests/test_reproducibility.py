"""Small regression check for seeded simulation reproducibility.

Run with:
    python ship_of_fools/tests/test_reproducibility.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


def _canonical_rows(rows):
    """Make NaN metrics comparable without hiding any finite-value changes."""
    canonical = []
    for row in rows:
        canonical.append({
            key: "NaN" if isinstance(value, float) and math.isnan(value) else value
            for key, value in row.items()
        })
    return canonical


def test_same_seed_reproduces_full_metric_trajectory():
    config = Config(n_agents=16, n_ticks=40, seed=1234)
    first = _canonical_rows(Simulation(config).run().to_rows())
    second = _canonical_rows(Simulation(config).run().to_rows())
    assert first == second


def test_different_seed_changes_stochastic_trajectory():
    first_config = Config(n_agents=16, n_ticks=40, seed=1234)
    second_config = Config(n_agents=16, n_ticks=40, seed=1235)
    first = _canonical_rows(Simulation(first_config).run().to_rows())
    second = _canonical_rows(Simulation(second_config).run().to_rows())
    assert first != second


if __name__ == "__main__":
    test_same_seed_reproduces_full_metric_trajectory()
    test_different_seed_changes_stochastic_trajectory()
    print("Seed reproducibility checks passed.")
