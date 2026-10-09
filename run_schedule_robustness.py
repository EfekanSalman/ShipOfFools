"""Compare shuffled action order with the completed fixed-order factorial run.

Reuses the pre-existing fixed-order seed summaries and trajectories, then runs
the same 120 seed-condition pairs under once-per-tick shuffled action order.
"""
import argparse
import csv
import json
import os
import random
import statistics
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.resource_factorial import ANALYSIS_METRICS, _mean_ci
from ship_of_fools.simulation.engine import Simulation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixed-dir", default="output/resource_factorial")
    parser.add_argument("--out-dir", default="output/schedule_robustness")
    parser.add_argument("--bootstrap-draws", type=int, default=10000)
    parser.add_argument("--analysis-seed", type=int, default=6102027)
    args = parser.parse_args()
    if args.bootstrap_draws < 1000:
        parser.error("--bootstrap-draws must be >=1000")

    os.makedirs(args.out_dir, exist_ok=True)
    fixed_path = os.path.join(args.fixed_dir, "seed_summaries.csv")
    with open(fixed_path, newline="", encoding="utf-8") as handle:
        fixed_rows = list(csv.DictReader(handle))
    if len(fixed_rows) != 120:
        parser.error(f"expected 120 fixed-order seed summaries, found {len(fixed_rows)}")

    payload = json.load(open(os.path.join(args.fixed_dir, "results.json"), encoding="utf-8"))
    base = Config(**payload["base_config"])
    if base.n_agents != 80 or base.n_ticks != 500:
        parser.error("source experiment does not match the pre-registered 80 x 500 design")

    summary_path = os.path.join(args.out_dir, "shuffled_seed_summaries.csv")
    series_path = os.path.join(args.out_dir, "shuffled_timeseries.csv")
    shuffled_rows = []
    fields = ["cell", "capacity", "regen_rate", "seed", "tick"] + list(ANALYSIS_METRICS)
    with open(series_path, "w", newline="", encoding="utf-8") as series_file:
        writer = csv.DictWriter(series_file, fieldnames=fields)
        writer.writeheader()
        for idx, fixed in enumerate(fixed_rows, start=1):
            config = Config(**payload["base_config"])
            config.seed = int(fixed["seed"])
            config.resource_capacity_per_agent = float(fixed["capacity"])
            fraction = payload["initial_stock_fraction_of_capacity"]
            config.initial_food_per_agent = config.resource_capacity_per_agent * fraction["food"]
            config.initial_water_per_agent = config.resource_capacity_per_agent * fraction["water"]
            config.food_regen_rate = float(fixed["regen_rate"])
            config.water_regen_rate = float(fixed["regen_rate"])
            config.agent_update_order = "shuffled"
            rows = Simulation(config).run().to_rows()
            tail = rows[-100:]
            summary = {
                "cell": fixed["cell"], "capacity": config.resource_capacity_per_agent,
                "regen_rate": config.food_regen_rate, "seed": config.seed,
                "final_population": int(rows[-1]["population"]),
            }
            for metric in ANALYSIS_METRICS:
                summary[f"mean_{metric}"] = statistics.fmean(float(row[metric]) for row in tail)
            shuffled_rows.append(summary)
            for row in rows:
                writer.writerow({"cell": fixed["cell"], "capacity": config.resource_capacity_per_agent,
                                 "regen_rate": config.food_regen_rate, "seed": config.seed,
                                 **{key: row[key] for key in ("tick",) + ANALYSIS_METRICS}})
            if idx % 10 == 0:
                print(f"Completed {idx}/120 shuffled runs", flush=True)

    with open(summary_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(shuffled_rows[0]))
        writer.writeheader()
        writer.writerows(shuffled_rows)

    fixed_by_key = {(row["cell"], int(row["seed"])): row for row in fixed_rows}
    shuffled_by_key = {(row["cell"], int(row["seed"])): row for row in shuffled_rows}
    rng = random.Random(args.analysis_seed)
    comparisons = {}
    for cell in sorted({row["cell"] for row in fixed_rows}):
        comparisons[cell] = {}
        for metric in ANALYSIS_METRICS:
            pairs = [(float(shuffled_by_key[(cell, int(row["seed"]))][f"mean_{metric}"]),
                      float(row[f"mean_{metric}"]))
                     for row in fixed_rows if row["cell"] == cell]
            differences = [shuffled - fixed for shuffled, fixed in pairs]
            comparisons[cell][metric] = {
                "n_paired_seeds": len(pairs),
                "fixed_mean": statistics.fmean(fixed for _, fixed in pairs),
                "shuffled_mean": statistics.fmean(shuffled for shuffled, _ in pairs),
                "shuffled_minus_fixed": statistics.fmean(differences),
                "paired_difference_sd": statistics.stdev(differences),
                "paired_difference_bootstrap_ci95": _mean_ci(differences, args.bootstrap_draws, rng),
            }

    result = {
        "experiment": "resource_factorial_schedule_robustness",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "design": "same 120 seed-condition pairs; fixed order reused from prior run; shuffled order rerun",
        "schedule": "living agents are shuffled once per tick using an independent scheduling RNG",
        "interpretation": "paired seed labels do not guarantee common random numbers after action order diverges",
        "metrics_window": "last 100 of 500 ticks",
        "bootstrap_draws": args.bootstrap_draws,
        "analysis_seed": args.analysis_seed,
        "comparisons": comparisons,
        "shuffled_seed_summaries_csv": "shuffled_seed_summaries.csv",
        "shuffled_timeseries_csv": "shuffled_timeseries.csv",
    }
    result_path = os.path.join(args.out_dir, "results.json")
    with open(result_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
    print(f"\nSaved schedule comparison: {result_path}")
    for cell, metrics in comparisons.items():
        print(f"\n{cell}")
        for metric in ("cooperation_rate", "conflict_rate", "true_scarcity"):
            item = metrics[metric]
            lo, hi = item["paired_difference_bootstrap_ci95"]
            print(f"  {metric}: shuffled-fixed={item['shuffled_minus_fixed']:+.3f} "
                  f"CI95=[{lo:+.3f}, {hi:+.3f}]")


if __name__ == "__main__":
    main()
