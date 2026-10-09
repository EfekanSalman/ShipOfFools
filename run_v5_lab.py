"""V5 demo: the counterfactual laboratory answering KNOWN_ISSUES.md ISSUE-007
("is the population collapse seen in V4 universal, or one seed's fluke?").

Three conditions, 10 seeds each, n_ticks=2000:
  A) default config              — the V4 baseline
  B) lower birth_rate_base       — naive "fewer babies should help" guess
  C) doubled resource capacity   — the actual bottleneck, per the finding below

Run this to reproduce the ISSUE-007 closing evidence in KNOWN_ISSUES.md.
Takes a few minutes (30 simulated worlds x 2000 ticks).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.counterfactual import run_seeds, extinction_rate
from ship_of_fools.experiments.causal_narrative import extract_narrative


def report(label, results, founder_pop):
    print(f"\n=== {label} ===")
    for i, r in enumerate(results):
        final_pop = r[-1].get("population", 0) if r else 0
        peak_pop = max(row.get("population", 0) for row in r) if r else 0
        print(f"  seed {i}: peak_pop={peak_pop:4d}  final_pop={final_pop:4d}")
    print(f"  fraction ending <=5 pop:        {extinction_rate(results, 5):.2f}")
    print(f"  fraction ending <=20 pop:       {extinction_rate(results, 20):.2f}")
    print(f"  fraction ending below founders: {extinction_rate(results, founder_pop):.2f}")


def main():
    base = Config(n_agents=80, n_ticks=2000)

    a = run_seeds(base, n_runs=10)
    report("A) default config", a, base.n_agents)

    b_config = Config(n_agents=80, n_ticks=2000, birth_rate_base=0.003)
    b = run_seeds(b_config, n_runs=10)
    report("B) lower birth_rate_base=0.003 (naive fix — makes it WORSE)", b, base.n_agents)

    c_config = Config(n_agents=80, n_ticks=2000, resource_capacity_per_agent=150.0,
                       initial_food_per_agent=100.0, initial_water_per_agent=100.0)
    c = run_seeds(c_config, n_runs=10)
    report("C) doubled resource capacity (the actual fix)", c, base.n_agents)

    print("\n=== Causal narrative for A) seed 0 (a representative collapse) ===")
    for line in extract_narrative(a[0], founder_population=base.n_agents):
        print(f"  {line}")


if __name__ == "__main__":
    main()
