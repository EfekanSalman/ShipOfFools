"""Re-test four earlier findings with a real significance test.

Each comparison: N seeds per condition (SAME seeds in both conditions), metric
= mean over the last 50 ticks of a 300-tick run (n_agents=60), Welch's t-test,
95% CI per condition, Cohen's d. The four:

  1. resource_capacity_per_agent 75 -> 150     (claimed dominant lever; sensitivity screen + ISSUE-007)
  2. identity_feedback_strength 0.0 -> 0.5     (claimed to erode trust, monotonic; ISSUE-004, was 5 seeds)
  3. reconciliation_bonus 0.0 -> 0.35          (claimed to improve avg_trust; ISSUE-005, was ONE seed)
  4. misinformation_rate 0.05 -> 0.35          (closed as "no reliable effect", ISSUE-001, was 8 seeds)

Results are printed AND written to output/revalidation_results.json so
REVALIDATION.md can quote them without retyping numbers.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation
from ship_of_fools.experiments.statistics import confidence_interval, welch_t_test, cohens_d

N_SEEDS = int(os.environ.get("REVAL_SEEDS", 30))
N_TICKS = 300
METRICS = ["true_scarcity", "population", "avg_trust", "inequality_gini", "conflict_rate"]

COMPARISONS = [
    ("resource_capacity_per_agent", {"resource_capacity_per_agent": 75.0, "initial_food_per_agent": 50.0, "initial_water_per_agent": 50.0},
                                     {"resource_capacity_per_agent": 150.0, "initial_food_per_agent": 100.0, "initial_water_per_agent": 100.0}),
    ("identity_feedback_strength", {"identity_feedback_strength": 0.0}, {"identity_feedback_strength": 0.5}),
    ("reconciliation_bonus", {"reconciliation_bonus": 0.0}, {"reconciliation_bonus": 0.35}),
    ("misinformation_rate", {"misinformation_rate": 0.05}, {"misinformation_rate": 0.35}),
]


def window_mean(rows, key, window=50):
    tail = rows[-window:]
    return sum(r[key] for r in tail) / len(tail)


def run_condition(overrides):
    out = {m: [] for m in METRICS}
    for seed in range(N_SEEDS):
        cfg = Config(n_agents=60, n_ticks=N_TICKS, seed=seed, **overrides)
        rows = Simulation(cfg).run().to_rows()
        for m in METRICS:
            out[m].append(window_mean(rows, m))
    return out


def main():
    t0 = time.time()
    results = {}
    for name, cond_a, cond_b in COMPARISONS:
        a, b = run_condition(cond_a), run_condition(cond_b)
        results[name] = {}
        print(f"\n=== {name}  (n={N_SEEDS} seeds/condition, {time.time()-t0:.0f}s elapsed) ===")
        print(f"{'metric':18s}{'A mean±CI95':>22s}{'B mean±CI95':>22s}{'Welch p':>11s}{'Cohen d':>10s}")
        for m in METRICS:
            ma, ha, _ = confidence_interval(a[m])
            mb, hb, _ = confidence_interval(b[m])
            _, p = welch_t_test(a[m], b[m])
            d = cohens_d(b[m], a[m])
            results[name][m] = {"A_mean": ma, "A_ci": ha, "B_mean": mb, "B_ci": hb, "p": p, "d": d}
            print(f"{m:18s}{ma:>13.3f}±{ha:<8.3f}{mb:>13.3f}±{hb:<8.3f}{p:>11.4f}{d:>10.2f}")
    os.makedirs("output", exist_ok=True)
    with open("output/revalidation_results.json", "w") as f:
        json.dump({"n_seeds": N_SEEDS, "n_ticks": N_TICKS, "results": results}, f, indent=1)
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
