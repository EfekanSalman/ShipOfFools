"""Run paired fixed/shuffled schedule experiments with independent agent RNGs."""
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
from ship_of_fools.experiments.resource_factorial import ANALYSIS_METRICS
from ship_of_fools.simulation.engine import Simulation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=500)
    parser.add_argument("--seeds-per-cell", type=int, default=30)
    parser.add_argument("--seed-start", type=int, default=40000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--out-dir", default="output/agent_rng_robustness")
    args = parser.parse_args()
    if args.agents <= 1 or args.ticks < args.window or args.seeds_per_cell < 2:
        parser.error("invalid agents, ticks/window, or seeds-per-cell")
    os.makedirs(args.out_dir, exist_ok=True)
    base = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0, agent_rng_mode="per_agent")
    summaries = []
    summary_path = os.path.join(args.out_dir, "seed_summaries.csv")
    series_path = os.path.join(args.out_dir, "timeseries.csv")
    fields = ["schedule", "cell", "capacity", "regen_rate", "seed", "tick"] + list(ANALYSIS_METRICS)
    with open(series_path, "w", newline="", encoding="utf-8") as series_file:
        writer = csv.DictWriter(series_file, fieldnames=fields)
        writer.writeheader()
        n_runs = 0
        for capacity in (90.0, 120.0):
            for regen in (0.016, 0.019):
                cell = f"C{int(capacity)}-R{str(regen).replace('.', 'p')}"
                cell_idx = ((0 if capacity == 90 else 2) + (0 if regen == 0.016 else 1))
                seeds = range(args.seed_start + cell_idx * args.seeds_per_cell,
                              args.seed_start + (cell_idx + 1) * args.seeds_per_cell)
                for seed in seeds:
                    for schedule in ("fixed", "shuffled"):
                        cfg = Config(**asdict(base))
                        cfg.seed = seed
                        cfg.agent_update_order = schedule
                        cfg.resource_capacity_per_agent = capacity
                        cfg.initial_food_per_agent = capacity * (2.0 / 3.0)
                        cfg.initial_water_per_agent = capacity * (2.0 / 3.0)
                        cfg.food_regen_rate = regen
                        cfg.water_regen_rate = regen
                        rows = Simulation(cfg).run().to_rows()
                        summary = {"schedule": schedule, "cell": cell, "capacity": capacity,
                                   "regen_rate": regen, "seed": seed,
                                   "final_population": int(rows[-1]["population"])}
                        tail = rows[-args.window:]
                        for metric in ANALYSIS_METRICS:
                            summary[f"mean_{metric}"] = sum(float(row[metric]) for row in tail) / len(tail)
                        summaries.append(summary)
                        for row in rows:
                            writer.writerow({"schedule": schedule, "cell": cell, "capacity": capacity,
                                             "regen_rate": regen, "seed": seed,
                                             **{key: row[key] for key in ("tick",) + ANALYSIS_METRICS}})
                        n_runs += 1
                        if n_runs % 10 == 0:
                            print(f"Completed {n_runs}/{8 * args.seeds_per_cell} runs", flush=True)
    with open(summary_path, "w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        w.writeheader()
        w.writerows(summaries)
    result = {
        "experiment": "paired_schedule_robustness_per_agent_rng",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "base_config": asdict(base),
        "design": "same seed for both schedules within each resource cell; independent per-agent action RNG streams",
        "schedule_rng": "separate stream derived deterministically from seed",
        "limits": "action-dependent random call counts can diverge within an agent after trajectories differ; this is not full potential-outcome coupling",
        "seeds_per_cell": args.seeds_per_cell,
        "seed_start": args.seed_start,
        "seed_end_inclusive": args.seed_start + 4 * args.seeds_per_cell - 1,
        "analysis_window": args.window,
        "raw_seed_summaries_csv": "seed_summaries.csv",
        "raw_timeseries_csv": "timeseries.csv",
    }
    with open(os.path.join(args.out_dir, "experiment.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
    print(f"Saved {len(summaries)} summaries to {args.out_dir}")


if __name__ == "__main__":
    main()
