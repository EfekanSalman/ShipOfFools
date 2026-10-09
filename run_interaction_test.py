"""Does resource_capacity_per_agent's effect depend on food_regen_rate's
level, or do they act independently? A full elementary-effects screen
(run_sensitivity.py) can't answer this by construction — this 2x2 factorial
design can, for this one pair (the two parameters the screen flagged as most
influential).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.sensitivity import factorial_interaction, HEADLINE_METRICS


def main():
    base = Config(n_agents=60)
    outcomes, main_a, main_b, interaction = factorial_interaction(
        base,
        "resource_capacity_per_agent", 50.0, 150.0,
        "food_regen_rate", 0.010, 0.024,
        n_runs=4, n_ticks=300,
    )

    print("=== 2x2 factorial: resource_capacity_per_agent x food_regen_rate ===\n")
    for name, vals in outcomes.items():
        print(f"{name:12s}" + "".join(f"  {m}={vals[m]:.3f}" for m in HEADLINE_METRICS))

    print(f"\n{'metric':22s}{'main effect A (capacity)':>26s}{'main effect B (regen)':>24s}{'interaction':>14s}")
    for m in HEADLINE_METRICS:
        print(f"{m:22s}{main_a[m]:26.3f}{main_b[m]:24.3f}{interaction[m]:14.3f}")

    print("\nRule of thumb: interaction is 'small' if |interaction| << |main effect A| and << |main effect B|.")


if __name__ == "__main__":
    main()
