"""Paired seed-block bootstrap for the 2x2x2 identity/resource experiment."""
import csv
import json
import random
import statistics


METRICS = ("avg_trust", "conflict_rate", "cooperation_rate", "true_scarcity",
           "inequality_gini", "population", "identity_formed_rate",
           "positive_relationship_rate")
RESOURCE_CELLS = ((90.0, 0.016), (90.0, 0.019), (120.0, 0.016), (120.0, 0.019))
N_DRAWS = 10000
ANALYSIS_SEED = 6102030


def percentile_ci(values):
    values = sorted(values)
    n = len(values)
    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return values[lo] * (hi - pos) + values[hi] * (pos - lo)
    return [q(0.025), q(0.975)]


def analyze(values_by_metric):
    rng = random.Random(ANALYSIS_SEED)
    result = {"bootstrap_draws": N_DRAWS, "analysis_seed": ANALYSIS_SEED,
              "seed_block_paired": True, "metrics": {}}
    for metric, data in values_by_metric.items():
        # data[(capacity, regen, identity)] = one observation per matched seed
        n = len(data[(90.0, 0.016, 0.0)])
        def identity_effects(indices):
            effects = {}
            for capacity, regen in RESOURCE_CELLS:
                low = statistics.fmean(data[(capacity, regen, 0.0)][i] for i in indices)
                high = statistics.fmean(data[(capacity, regen, 0.5)][i] for i in indices)
                effects[(capacity, regen)] = high - low
            cap_low, cap_high = 90.0, 120.0
            regen_low, regen_high = 0.016, 0.019
            return {
                "by_resource_cell": effects,
                "identity_average": statistics.fmean(effects.values()),
                "identity_by_capacity": (effects[(cap_high, regen_low)] + effects[(cap_high, regen_high)]) / 2
                                       - (effects[(cap_low, regen_low)] + effects[(cap_low, regen_high)]) / 2,
                "identity_by_regen": (effects[(cap_low, regen_high)] + effects[(cap_high, regen_high)]) / 2
                                    - (effects[(cap_low, regen_low)] + effects[(cap_high, regen_low)]) / 2,
                "identity_by_capacity_by_regen": (effects[(cap_high, regen_high)] - effects[(cap_high, regen_low)])
                                                - (effects[(cap_low, regen_high)] - effects[(cap_low, regen_low)]),
            }

        point = identity_effects(list(range(n)))
        names = ("identity_average", "identity_by_capacity", "identity_by_regen",
                 "identity_by_capacity_by_regen")
        draws = {name: [] for name in names}
        cell_draws = {cell: [] for cell in RESOURCE_CELLS}
        for _ in range(N_DRAWS):
            sampled = [rng.randrange(n) for _ in range(n)]
            current = identity_effects(sampled)
            for name in names:
                draws[name].append(current[name])
            for cell in RESOURCE_CELLS:
                cell_draws[cell].append(current["by_resource_cell"][cell])
        metric_result = {
            "n_seed_blocks": n,
            "identity_effect_by_resource_cell": {},
            "identity_resource_contrasts": {},
        }
        for cell in RESOURCE_CELLS:
            key = f"C{int(cell[0])}-R{str(cell[1]).replace('.', 'p')}"
            metric_result["identity_effect_by_resource_cell"][key] = {
                "estimate": point["by_resource_cell"][cell],
                "bootstrap_ci95": percentile_ci(cell_draws[cell]),
            }
        for name in names:
            metric_result["identity_resource_contrasts"][name] = {
                "estimate": point[name], "bootstrap_ci95": percentile_ci(draws[name])
            }
        result["metrics"][metric] = metric_result
    return result


def main():
    with open("output/identity_resource_factorial/seed_summaries.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    expected = 8 * 30
    if len(rows) != expected:
        raise ValueError(f"expected {expected} rows; found {len(rows)}")
    seeds = sorted({int(row["seed"]) for row in rows})
    if len(seeds) != 30:
        raise ValueError(f"expected 30 seed blocks; found {len(seeds)}")
    lookup = {}
    for row in rows:
        key = (float(row["capacity"]), float(row["regen_rate"]),
               float(row["identity_feedback_strength"]), int(row["seed"]))
        lookup[key] = row
    required = {(c, r, i, seed) for c, r in RESOURCE_CELLS for i in (0.0, 0.5) for seed in seeds}
    if lookup.keys() != required:
        raise ValueError("incomplete or duplicated factorial seed blocks")

    values_by_metric = {}
    for metric in METRICS:
        values_by_metric[metric] = {
            (c, r, i): [float(lookup[(c, r, i, seed)][f"mean_{metric}"]) for seed in seeds]
            for c, r in RESOURCE_CELLS for i in (0.0, 0.5)
        }
    result = analyze(values_by_metric)
    result["primary_metrics"] = ["avg_trust", "conflict_rate", "cooperation_rate"]
    result["secondary_metrics"] = [m for m in METRICS if m not in result["primary_metrics"]]
    with open("output/identity_resource_factorial/analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    for metric in result["primary_metrics"]:
        print(f"\n{metric}")
        for name, value in result["metrics"][metric]["identity_resource_contrasts"].items():
            low, high = value["bootstrap_ci95"]
            print(f"  {name}: {value['estimate']:+.4f} CI95=[{low:+.4f}, {high:+.4f}]")
        print("  per resource cell")
        for cell, value in result["metrics"][metric]["identity_effect_by_resource_cell"].items():
            low, high = value["bootstrap_ci95"]
            print(f"    {cell}: {value['estimate']:+.4f} CI95=[{low:+.4f}, {high:+.4f}]")


if __name__ == "__main__":
    main()
