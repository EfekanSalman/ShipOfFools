"""Add bootstrap resource-factorial contrasts for fixed vs shuffled schedules."""
import csv
import json
import os
import random
import statistics

from ship_of_fools.experiments.resource_factorial import _factorial_contrasts, _mean_ci


def main():
    fixed_dir = "output/resource_factorial"
    result_dir = "output/schedule_robustness"
    with open(os.path.join(fixed_dir, "seed_summaries.csv"), newline="", encoding="utf-8") as f:
        fixed = list(csv.DictReader(f))
    with open(os.path.join(result_dir, "shuffled_seed_summaries.csv"), newline="", encoding="utf-8") as f:
        shuffled = list(csv.DictReader(f))
    fixed_map = {(r["cell"], int(r["seed"])): r for r in fixed}
    shuffled_map = {(r["cell"], int(r["seed"])): r for r in shuffled}
    if fixed_map.keys() != shuffled_map.keys() or len(fixed_map) != 120:
        raise ValueError("fixed and shuffled runs must have the same 120 cell-seed pairs")

    rng = random.Random(6102028)
    cell_names = sorted({key[0] for key in fixed_map})
    output = {}
    for metric in ("cooperation_rate", "conflict_rate", "true_scarcity"):
        field = f"mean_{metric}"
        paired = {cell: [(float(shuffled_map[(cell, seed)][field]), float(fixed_map[(cell, seed)][field]))
                         for _, seed in sorted(key for key in fixed_map if key[0] == cell)]
                  for cell in cell_names}
        fmeans = {cell: statistics.fmean(pair[1] for pair in pairs) for cell, pairs in paired.items()}
        smeans = {cell: statistics.fmean(pair[0] for pair in pairs) for cell, pairs in paired.items()}
        fcontrast = _factorial_contrasts(fmeans)
        scontrast = _factorial_contrasts(smeans)
        boot = {"fixed": {name: [] for name in fcontrast}, "shuffled": {name: [] for name in fcontrast},
                "delta": {name: [] for name in fcontrast}}
        for _ in range(10000):
            fdraw, sdraw = {}, {}
            for cell, pairs in paired.items():
                sampled = [pairs[rng.randrange(len(pairs))] for _ in pairs]
                sdraw[cell] = statistics.fmean(x[0] for x in sampled)
                fdraw[cell] = statistics.fmean(x[1] for x in sampled)
            fc, sc = _factorial_contrasts(fdraw), _factorial_contrasts(sdraw)
            for name in fcontrast:
                boot["fixed"][name].append(fc[name])
                boot["shuffled"][name].append(sc[name])
                boot["delta"][name].append(sc[name] - fc[name])
        output[metric] = {}
        for name in fcontrast:
            deltas = boot["delta"][name]
            deltas.sort()
            output[metric][name] = {
                "fixed_estimate": fcontrast[name],
                "shuffled_estimate": scontrast[name],
                "shuffled_minus_fixed": scontrast[name] - fcontrast[name],
                "fixed_bootstrap_ci95": _percentile_ci(boot["fixed"][name]),
                "shuffled_bootstrap_ci95": _percentile_ci(boot["shuffled"][name]),
                "paired_delta_bootstrap_ci95": _percentile_ci(deltas),
            }

    path = os.path.join(result_dir, "results.json")
    with open(path, encoding="utf-8") as f:
        result = json.load(f)
    result["factorial_contrast_comparison"] = output
    result["contrast_bootstrap"] = "10000 paired seed-level resamples within each cell"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    for metric, contrasts in output.items():
        print(f"\n{metric}")
        for name, row in contrasts.items():
            lo, hi = row["paired_delta_bootstrap_ci95"]
            print(f"  {name}: fixed={row['fixed_estimate']:+.3f} shuffled={row['shuffled_estimate']:+.3f} "
                  f"delta={row['shuffled_minus_fixed']:+.3f} delta-CI95=[{lo:+.3f}, {hi:+.3f}]")


def _percentile_ci(values):
    values = sorted(values)
    n = len(values)
    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return values[lo] * (hi - pos) + values[hi] * (pos - lo)
    return [q(0.025), q(0.975)]


if __name__ == "__main__":
    main()
