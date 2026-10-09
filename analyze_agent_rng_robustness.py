"""Analyze paired fixed-vs-shuffled schedule runs with per-agent RNG streams."""
import csv
import json
import random
import statistics

from ship_of_fools.experiments.resource_factorial import _factorial_contrasts


METRICS = ("cooperation_rate", "conflict_rate", "true_scarcity")
CELLS = ("C90-R0p016", "C90-R0p019", "C120-R0p016", "C120-R0p019")


def ci(values):
    values.sort()
    n = len(values)
    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return values[lo] * (hi - pos) + values[hi] * (pos - lo)
    return [q(0.025), q(0.975)]


def contrasts(means):
    ll, lh, hl, hh = [means[cell] for cell in CELLS]
    return {
        "capacity_high_minus_low": ((hl + hh) - (ll + lh)) / 2,
        "regen_high_minus_low": ((lh + hh) - (ll + hl)) / 2,
        "capacity_by_regen_interaction": (hh - hl) - (lh - ll),
    }


def main():
    with open("output/agent_rng_robustness/seed_summaries.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    data = {}
    for row in rows:
        key = (row["schedule"], row["cell"], int(row["seed"]))
        data[key] = row
    expected = 240
    if len(data) != expected:
        raise ValueError(f"expected {expected} schedule-cell-seed records, found {len(data)}")
    seedsets = {cell: sorted(seed for schedule, c, seed in data if c == cell and schedule == "fixed")
                for cell in CELLS}
    for cell in CELLS:
        if seedsets[cell] != sorted(seed for schedule, c, seed in data if c == cell and schedule == "shuffled"):
            raise ValueError(f"fixed/shuffled seed mismatch for {cell}")

    rng = random.Random(6102029)
    result = {"design": "paired seed bootstrap, resampled within each resource cell",
              "bootstrap_draws": 10000, "analysis_seed": 6102029, "metrics": {}}
    for metric in METRICS:
        field = f"mean_{metric}"
        pairs = {cell: [(float(data[("fixed", cell, seed)][field]),
                        float(data[("shuffled", cell, seed)][field]))
                        for seed in seedsets[cell]] for cell in CELLS}
        fixed_means = {cell: statistics.fmean(pair[0] for pair in p) for cell, p in pairs.items()}
        shuffled_means = {cell: statistics.fmean(pair[1] for pair in p) for cell, p in pairs.items()}
        fixed_contrasts = contrasts(fixed_means)
        shuffled_contrasts = contrasts(shuffled_means)
        cell_results = {}
        for cell in CELLS:
            diffs = [shuffled - fixed for fixed, shuffled in pairs[cell]]
            draws = [statistics.fmean(diffs[rng.randrange(len(diffs))] for _ in diffs)
                     for _ in range(10000)]
            cell_results[cell] = {
                "fixed_mean": fixed_means[cell], "shuffled_mean": shuffled_means[cell],
                "shuffled_minus_fixed": statistics.fmean(diffs),
                "paired_difference_ci95": ci(draws),
                "paired_difference_sd": statistics.stdev(diffs),
            }
        effect_results = {}
        effect_draws = {name: [] for name in fixed_contrasts}
        for _ in range(10000):
            fmeans, smeans = {}, {}
            for cell, cell_pairs in pairs.items():
                sample = [cell_pairs[rng.randrange(len(cell_pairs))] for _ in cell_pairs]
                fmeans[cell] = statistics.fmean(pair[0] for pair in sample)
                smeans[cell] = statistics.fmean(pair[1] for pair in sample)
            fc, sc = contrasts(fmeans), contrasts(smeans)
            for name in effect_draws:
                effect_draws[name].append(sc[name] - fc[name])
        for name in fixed_contrasts:
            effect_results[name] = {
                "fixed_estimate": fixed_contrasts[name],
                "shuffled_estimate": shuffled_contrasts[name],
                "shuffled_minus_fixed": shuffled_contrasts[name] - fixed_contrasts[name],
                "paired_delta_ci95": ci(effect_draws[name]),
            }
        result["metrics"][metric] = {"cells": cell_results, "factorial_effects": effect_results}

    with open("output/agent_rng_robustness/analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    for metric, info in result["metrics"].items():
        print(f"\n{metric}")
        for name, item in info["factorial_effects"].items():
            lo, hi = item["paired_delta_ci95"]
            print(f"  {name}: fixed={item['fixed_estimate']:+.3f} shuffled={item['shuffled_estimate']:+.3f} "
                  f"delta={item['shuffled_minus_fixed']:+.3f} CI95=[{lo:+.3f}, {hi:+.3f}]")


if __name__ == "__main__":
    main()
