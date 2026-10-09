"""Run a pre-specified 2x2 resource by decision-arm experiment.

Defaults reproduce the 2x2x3 scarcity-link ablation; --arms selects other arms.
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
from ship_of_fools.simulation.engine import Simulation


ACTIONS = ("forage", "rest", "socialize", "share", "steal", "spread_belief")
LABELS = ("leader", "benefactor", "opportunist", "survivor")
METRICS = (("conflict_rate", "cooperation_rate", "true_scarcity", "avg_scarcity_belief",
            "avg_stress", "avg_trust", "inequality_gini", "population", "helping_norm")
           + tuple(f"action_{name}_rate" for name in ACTIONS)
           + tuple(f"identity_{name}_rate" for name in LABELS)
           + ("avg_wealth",))  # appended last so earlier metrics keep their bootstrap draws
CAPACITIES = (90.0, 120.0)
REGEN_RATES = (0.016, 0.019)
ARMS = {
    "intact": {},
    "zero": {"steal_scarcity_weight": 0.0, "share_scarcity_weight": 0.0},
    "fixed": {"action_scarcity_reference": 0.5},
    "need_based": {"decision_architecture": "need_based"},
}
DEFAULT_ARMS = "intact,zero,fixed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=500)
    parser.add_argument("--seeds-per-cell", type=int, default=30)
    parser.add_argument("--seed-start", type=int, default=60000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--out-dir", default="output/scarcity_link_ablation")
    parser.add_argument("--arms", default=DEFAULT_ARMS, help="comma-separated arm names; the first is the reference")
    parser.add_argument("--protocol", default="EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md")
    args = parser.parse_args()
    arm_names = args.arms.split(",")
    if len(set(arm_names)) != len(arm_names) or any(name not in ARMS for name in arm_names):
        parser.error(f"arms must be distinct names from {sorted(ARMS)}")
    arms = {name: ARMS[name] for name in arm_names}
    if args.agents <= 1 or args.ticks < args.window or args.seeds_per_cell < 2:
        parser.error("invalid agents, ticks/window, or seeds-per-cell")
    os.makedirs(args.out_dir, exist_ok=True)
    base = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0,
                  agent_update_order="fixed", agent_rng_mode="shared")
    summaries = []
    summary_path = os.path.join(args.out_dir, "seed_summaries.csv")
    series_path = os.path.join(args.out_dir, "timeseries.csv")
    fields = ["capacity", "regen_rate", "arm", "cell", "seed", "tick"] + list(METRICS)
    total = len(CAPACITIES) * len(REGEN_RATES) * len(arms) * args.seeds_per_cell
    with open(series_path, "w", newline="", encoding="utf-8") as series_file:
        writer = csv.DictWriter(series_file, fieldnames=fields)
        writer.writeheader()
        n_runs = 0
        for capacity in CAPACITIES:
            for regen in REGEN_RATES:
                for arm, overrides in arms.items():
                    cell = f"C{int(capacity)}-R{str(regen).replace('.', 'p')}-{arm}"
                    for seed in range(args.seed_start, args.seed_start + args.seeds_per_cell):
                        cfg = Config(**asdict(base))
                        cfg.seed = seed
                        cfg.resource_capacity_per_agent = capacity
                        cfg.initial_food_per_agent = capacity * (2.0 / 3.0)
                        cfg.initial_water_per_agent = capacity * (2.0 / 3.0)
                        cfg.food_regen_rate = regen
                        cfg.water_regen_rate = regen
                        for key, value in overrides.items():
                            setattr(cfg, key, value)
                        rows = Simulation(cfg).run().to_rows()
                        tail = rows[-args.window:]
                        summary = {"capacity": capacity, "regen_rate": regen, "arm": arm,
                                   "cell": cell, "seed": seed,
                                   "final_population": int(rows[-1]["population"])}
                        for metric in METRICS:
                            summary[f"mean_{metric}"] = sum(float(r[metric]) for r in tail) / len(tail)
                        summaries.append(summary)
                        for row in rows:
                            writer.writerow({"capacity": capacity, "regen_rate": regen, "arm": arm,
                                             "cell": cell, "seed": seed,
                                             **{key: row[key] for key in ("tick",) + METRICS}})
                        n_runs += 1
                        if n_runs % 10 == 0:
                            print(f"Completed {n_runs}/{total} runs", flush=True)
    with open(summary_path, "w", newline="", encoding="utf-8") as handle:
        out = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        out.writeheader()
        out.writerows(summaries)
    metadata = {
        "experiment": "resource_2x2_x_decision_arm",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(), "base_config": asdict(base),
        "capacities": list(CAPACITIES), "food_and_water_regen_rates": list(REGEN_RATES),
        "arms": arms,
        "seeds_per_cell": args.seeds_per_cell, "seed_start": args.seed_start,
        "seed_end_inclusive": args.seed_start + args.seeds_per_cell - 1,
        "seed_assignment": "same seed block used across all cells",
        "analysis_unit": "seed-level mean over final window; ticks are not replicates",
        "analysis_window": args.window, "protocol": args.protocol,
        "metrics": list(METRICS), "seed_summaries_csv": "seed_summaries.csv",
        "timeseries_csv": "timeseries.csv",
    }
    with open(os.path.join(args.out_dir, "experiment.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, allow_nan=False)
    print(f"Saved {len(summaries)} seed-condition summaries to {args.out_dir}")


if __name__ == "__main__":
    main()
