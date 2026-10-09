"""Paired seed-block bootstrap for a 2x2 resource by decision-arm experiment.

Arms are read from the seed summaries; the first arm in the file is the reference.
"""
import argparse
import csv
import json
import os
import random
import statistics


PRIMARY = ("conflict_rate", "cooperation_rate")
MANIPULATION_CHECK = ("true_scarcity", "avg_scarcity_belief")
RESOURCE_CELLS = ((90.0, 0.016), (90.0, 0.019), (120.0, 0.016), (120.0, 0.019))
ARMS = ("intact", "zero", "fixed")
CONTRASTS = ("capacity_high_minus_low", "regen_high_minus_low", "capacity_by_regen_interaction")
RETAINED = ("capacity_high_minus_low", "regen_high_minus_low")
N_DRAWS = 10000
ANALYSIS_SEED = 6102607


def percentile_ci(values):
    values = sorted(values)
    n = len(values)
    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return values[lo] * (hi - pos) + values[hi] * (pos - lo)
    return [q(0.025), q(0.975)]


def contrasts(data, arm, indices):
    """2x2 high-minus-low resource contrasts within one arm over the given seed blocks."""
    m = {cell: statistics.fmean(data[(cell[0], cell[1], arm)][i] for i in indices)
         for cell in RESOURCE_CELLS}
    ll, lh, hl, hh = (m[cell] for cell in RESOURCE_CELLS)
    return {
        "capacity_high_minus_low": (hl + hh) / 2 - (ll + lh) / 2,
        "regen_high_minus_low": (lh + hh) / 2 - (ll + hl) / 2,
        "capacity_by_regen_interaction": (hh - hl) - (lh - ll),
    }


def analyze(values_by_metric, n_draws=N_DRAWS, analysis_seed=ANALYSIS_SEED, arms=ARMS, factorial=None):
    """Bootstrap resource contrasts per arm.

    factorial, if given, names three arms (a_only, b_only, both) that form a
    2x2 with the reference arm; each resource contrast is then split into the
    main effects of the two arm factors and their interaction.
    """
    reference = arms[0]
    rng = random.Random(analysis_seed)
    result = {"bootstrap_draws": n_draws, "analysis_seed": analysis_seed,
              "seed_block_paired": True, "reference_arm": reference, "metrics": {}}
    for metric, data in values_by_metric.items():
        # data[(capacity, regen, arm)] = one observation per matched seed
        n = len(data[(90.0, 0.016, reference)])
        everyone = list(range(n))
        point = {arm: contrasts(data, arm, everyone) for arm in arms}
        draws = {arm: {name: [] for name in CONTRASTS} for arm in arms}
        for _ in range(n_draws):
            sampled = [rng.randrange(n) for _ in range(n)]
            for arm in arms:
                current = contrasts(data, arm, sampled)
                for name in CONTRASTS:
                    draws[arm][name].append(current[name])
        metric_result = {"n_seed_blocks": n, "cell_means": {}, "arms": {}}
        for arm in arms:
            for capacity, regen in RESOURCE_CELLS:
                values = data[(capacity, regen, arm)]
                key = f"C{int(capacity)}-R{str(regen).replace('.', 'p')}-{arm}"
                metric_result["cell_means"][key] = {
                    "mean": statistics.fmean(values), "sd_between_seeds": statistics.stdev(values)}
            arm_result = {"contrasts": {}}
            for name in CONTRASTS:
                arm_result["contrasts"][name] = {
                    "estimate": point[arm][name], "bootstrap_ci95": percentile_ci(draws[arm][name])}
            if arm != reference:
                arm_result["minus_intact"] = {}
                arm_result["retained_fraction"] = {}
                for name in CONTRASTS:
                    diff = [a - b for a, b in zip(draws[arm][name], draws[reference][name])]
                    arm_result["minus_intact"][name] = {
                        "estimate": point[arm][name] - point[reference][name],
                        "bootstrap_ci95": percentile_ci(diff)}
                for name in RETAINED:
                    ratio = [a / b for a, b in zip(draws[arm][name], draws[reference][name]) if b != 0]
                    if point[reference][name] == 0 or not ratio:
                        continue  # undefined when the intact arm shows no effect
                    arm_result["retained_fraction"][name] = {
                        "estimate": point[arm][name] / point[reference][name],
                        "bootstrap_ci95": percentile_ci(ratio)}
            metric_result["arms"][arm] = arm_result
        if factorial is not None:
            a_only, b_only, both = factorial
            def split(ref, a, b, ab):
                return {"a_main_effect": ((a - ref) + (ab - b)) / 2,
                        "b_main_effect": ((b - ref) + (ab - a)) / 2,
                        "a_by_b_interaction": (ab - b) - (a - ref)}
            metric_result["arm_factorial"] = {"a": a_only, "b": b_only, "both": both, "contrasts": {}}
            for name in CONTRASTS:
                estimate = split(point[reference][name], point[a_only][name], point[b_only][name], point[both][name])
                rows = [split(*values) for values in zip(draws[reference][name], draws[a_only][name],
                                                         draws[b_only][name], draws[both][name])]
                metric_result["arm_factorial"]["contrasts"][name] = {
                    key: {"estimate": estimate[key], "bootstrap_ci95": percentile_ci([row[key] for row in rows])}
                    for key in estimate}
        result["metrics"][metric] = metric_result
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default="output/scarcity_link_ablation")
    parser.add_argument("--seeds-per-cell", type=int, default=30)
    parser.add_argument("--factorial", default=None,
                        help="A_ONLY,B_ONLY,BOTH: arms forming a 2x2 with the reference arm")
    args = parser.parse_args()
    with open(os.path.join(args.dir, "seed_summaries.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seeds = sorted({int(row["seed"]) for row in rows})
    if len(seeds) != args.seeds_per_cell:
        raise ValueError(f"expected {args.seeds_per_cell} seed blocks; found {len(seeds)}")
    arms = tuple(dict.fromkeys(row["arm"] for row in rows))
    lookup = {(float(row["capacity"]), float(row["regen_rate"]), row["arm"], int(row["seed"])): row
              for row in rows}
    required = {(c, r, arm, seed) for c, r in RESOURCE_CELLS for arm in arms for seed in seeds}
    if lookup.keys() != required or len(rows) != len(required):
        raise ValueError("incomplete or duplicated factorial seed blocks")

    metrics = [key[len("mean_"):] for key in rows[0] if key.startswith("mean_")]
    values_by_metric = {
        metric: {(c, r, arm): [float(lookup[(c, r, arm, seed)][f"mean_{metric}"]) for seed in seeds]
                 for c, r in RESOURCE_CELLS for arm in arms}
        for metric in metrics
    }
    factorial = tuple(args.factorial.split(",")) if args.factorial else None
    if factorial is not None and (len(factorial) != 3 or any(name not in arms[1:] for name in factorial)):
        raise ValueError("--factorial needs three non-reference arm names present in the data")
    result = analyze(values_by_metric, arms=arms, factorial=factorial)
    result["primary_metrics"] = list(PRIMARY)
    result["manipulation_check_metrics"] = list(MANIPULATION_CHECK)
    result["secondary_metrics"] = [m for m in metrics if m not in PRIMARY + MANIPULATION_CHECK]
    with open(os.path.join(args.dir, "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    for metric in PRIMARY + MANIPULATION_CHECK:
        print(f"\n{metric}")
        for arm in arms:
            arm_result = result["metrics"][metric]["arms"][arm]
            for name in CONTRASTS:
                value = arm_result["contrasts"][name]
                low, high = value["bootstrap_ci95"]
                line = f"  {arm:10s} {name}: {value['estimate']:+.4f} CI95=[{low:+.4f}, {high:+.4f}]"
                if name in arm_result.get("retained_fraction", {}):
                    kept = arm_result["retained_fraction"][name]
                    line += (f"  retained={kept['estimate']:+.2f} "
                             f"[{kept['bootstrap_ci95'][0]:+.2f}, {kept['bootstrap_ci95'][1]:+.2f}]")
                print(line)
        if factorial is not None:
            split = result["metrics"][metric]["arm_factorial"]
            for name in CONTRASTS:
                parts = "  ".join(
                    "{}={:+.4f} [{:+.4f}, {:+.4f}]".format(key, value["estimate"], *value["bootstrap_ci95"])
                    for key, value in split["contrasts"][name].items())
                print("  split of {} (a={}, b={}): {}".format(name, split["a"], split["b"], parts))


if __name__ == "__main__":
    main()
