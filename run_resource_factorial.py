"""Run the pre-specified 2x2 resource-regime experiment.

The default run is 120 worlds (30 seeds x 4 conditions, 80 agents, 500 ticks)
and may take several minutes.
"""
import argparse
import csv
import json
import os
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.resource_factorial import ANALYSIS_METRICS, run_resource_factorial


def parse_levels(raw):
    try:
        values = [float(value.strip()) for value in raw.split(",") if value.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("levels must be comma-separated numbers") from exc
    if len(values) != 2 or len(set(values)) != 2:
        raise argparse.ArgumentTypeError("provide exactly two distinct levels")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=500)
    parser.add_argument("--seeds-per-cell", type=int, default=30)
    parser.add_argument("--seed-start", type=int, default=30000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--capacities", type=parse_levels, default=[90.0, 120.0])
    parser.add_argument("--regen-rates", type=parse_levels, default=[0.016, 0.019])
    parser.add_argument("--bootstrap-draws", type=int, default=10000)
    parser.add_argument("--analysis-seed", type=int, default=6102026)
    parser.add_argument("--out-dir", default="output/resource_factorial")
    args = parser.parse_args()
    if args.agents <= 1 or args.ticks <= 0:
        parser.error("--agents must be >1 and --ticks must be positive")
    if args.seeds_per_cell < 2 or not 0 < args.window <= args.ticks:
        parser.error("--seeds-per-cell must be >=2 and --window in 1..--ticks")
    if args.bootstrap_draws < 1000:
        parser.error("--bootstrap-draws must be >=1000")

    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    base_config = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0)
    time_path = os.path.join(out_dir, "timeseries.csv")
    summary_path = os.path.join(out_dir, "seed_summaries.csv")
    json_path = os.path.join(out_dir, "results.json")
    elapsed_runs = 0
    writer = None
    time_file = open(time_path, "w", newline="", encoding="utf-8")

    def save_timeseries(cell_id, capacity, regen, seed, rows):
        nonlocal elapsed_runs, writer
        if writer is None:
            fieldnames = ["cell", "capacity", "regen_rate", "seed"] + list(rows[0].keys())
            writer = csv.DictWriter(time_file, fieldnames=fieldnames)
            writer.writeheader()
        for row in rows:
            writer.writerow({"cell": cell_id, "capacity": capacity,
                             "regen_rate": regen, "seed": seed, **row})
        elapsed_runs += 1
        if elapsed_runs % 10 == 0:
            print(f"Completed {elapsed_runs}/" +
                  f"{4 * args.seeds_per_cell} simulation runs", flush=True)

    try:
        results = run_resource_factorial(
            base_config,
            capacities=args.capacities,
            regen_rates=args.regen_rates,
            n_runs=args.seeds_per_cell,
            seed_start=args.seed_start,
            analysis_window=args.window,
            bootstrap_draws=args.bootstrap_draws,
            analysis_seed=args.analysis_seed,
            on_run_complete=save_timeseries,
        )
    finally:
        time_file.close()

    seed_summaries = [
        summary
        for cell in results["cells"].values()
        for summary in cell["seed_summaries"]
    ]
    with open(summary_path, "w", newline="", encoding="utf-8") as handle:
        fields = ["cell", "capacity", "regen_rate", "seed", "final_population"] + [
            f"mean_{metric}" for metric in ANALYSIS_METRICS
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(seed_summaries)

    payload = {
        "experiment": "resource_scarcity_cooperation_conflict_2x2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "base_config": asdict(base_config),
        "capacity_levels": args.capacities,
        "food_and_water_regen_levels": args.regen_rates,
        "initial_stock_fraction_of_capacity": {
            "food": base_config.initial_food_per_agent / base_config.resource_capacity_per_agent,
            "water": base_config.initial_water_per_agent / base_config.resource_capacity_per_agent,
        },
        "seeds_per_cell": args.seeds_per_cell,
        "seed_start": args.seed_start,
        "seed_end_inclusive": args.seed_start + 4 * args.seeds_per_cell - 1,
        "seed_assignment": "disjoint sequential seed blocks per cell; not paired common-random-numbers",
        "result_unit": "one simulation seed; per-tick values are averaged within each seed",
        "protocol": "EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md",
        "results": results,
        "raw_timeseries_csv": "timeseries.csv",
        "seed_summaries_csv": "seed_summaries.csv",
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, allow_nan=False)

    print("\nCell means +/- 95% bootstrap CI (seed is the unit):")
    for metric in ("cooperation_rate", "conflict_rate", "true_scarcity"):
        print(f"\n{metric}")
        for cell_id, summary in results["cell_statistics"][metric].items():
            low, high = summary["bootstrap_ci95"]
            print(f"  {cell_id:10s} n={summary['n_seeds']:2d} "
                  f"mean={summary['mean']:.3f} sd={summary['sd_between_seeds']:.3f} "
                  f"CI95=[{low:.3f}, {high:.3f}]")
    print("\nFactorial contrasts (high minus low; interaction is difference-in-differences):")
    for metric in ("cooperation_rate", "conflict_rate", "true_scarcity"):
        print(f"  {metric}")
        for name, value in results["factorial_effects"][metric].items():
            low, high = value["bootstrap_ci95"]
            print(f"    {name:34s} estimate={value['estimate']:.3f} "
                  f"CI95=[{low:.3f}, {high:.3f}]")
    print(f"\nSaved:")
    print(f"  {json_path}")
    print(f"  {summary_path}")
    print(f"  {time_path}")


if __name__ == "__main__":
    main()
