"""Post hoc follow-up: identity-label and action shares in the 2x2x2 identity experiment.

Re-runs the same 240 worlds as run_identity_resource_factorial.py (same configs
and seeds, so the trajectories are identical) and records columns the original
run did not save. Exploratory; not part of the pre-specified protocol.
"""
import argparse
import csv
import json
import os
import statistics
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(__file__))
from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


ACTIONS = ("forage", "rest", "socialize", "share", "steal", "spread_belief")
LABELS = ("leader", "benefactor", "opportunist", "survivor")
METRICS = (("conflict_rate", "inequality_gini", "population", "identity_formed_rate")
           + tuple(f"identity_{name}_rate" for name in LABELS)
           + tuple(f"action_{name}_rate" for name in ACTIONS))
RESOURCE_CELLS = ((90.0, 0.016), (90.0, 0.019), (120.0, 0.016), (120.0, 0.019))
IDENTITY_LEVELS = (0.0, 0.5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=500)
    parser.add_argument("--seeds-per-cell", type=int, default=30)
    parser.add_argument("--seed-start", type=int, default=50000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--out-dir", default="output/identity_label_followup")
    parser.add_argument("--original", default="output/identity_resource_factorial/seed_summaries.csv",
                        help="original seed summaries, used to confirm the re-run reproduces them")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    original = {}
    if os.path.exists(args.original):
        with open(args.original, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = (float(row["capacity"]), float(row["regen_rate"]),
                       float(row["identity_feedback_strength"]), int(row["seed"]))
                original[key] = float(row["mean_conflict_rate"])

    base = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0,
                  agent_update_order="fixed", agent_rng_mode="shared")
    summaries = []
    checked = 0
    for capacity, regen in RESOURCE_CELLS:
        for identity in IDENTITY_LEVELS:
            for seed in range(args.seed_start, args.seed_start + args.seeds_per_cell):
                cfg = Config(**asdict(base))
                cfg.seed = seed
                cfg.resource_capacity_per_agent = capacity
                cfg.initial_food_per_agent = capacity * (2.0 / 3.0)
                cfg.initial_water_per_agent = capacity * (2.0 / 3.0)
                cfg.food_regen_rate = regen
                cfg.water_regen_rate = regen
                cfg.identity_feedback_strength = identity
                tail = Simulation(cfg).run().to_rows()[-args.window:]
                summary = {"capacity": capacity, "regen_rate": regen,
                           "identity_feedback_strength": identity, "seed": seed}
                for metric in METRICS:
                    summary[f"mean_{metric}"] = sum(float(r[metric]) for r in tail) / len(tail)
                key = (capacity, regen, identity, seed)
                if key in original:
                    if abs(original[key] - summary["mean_conflict_rate"]) > 1e-12:
                        raise RuntimeError(f"re-run does not reproduce the original run for {key}")
                    checked += 1
                summaries.append(summary)
                if len(summaries) % 10 == 0:
                    print(f"Completed {len(summaries)}/{8 * args.seeds_per_cell} runs", flush=True)

    with open(os.path.join(args.out_dir, "seed_summaries.csv"), "w", newline="", encoding="utf-8") as f:
        out = csv.DictWriter(f, fieldnames=list(summaries[0]))
        out.writeheader()
        out.writerows(summaries)

    table = {}
    for capacity, regen in RESOURCE_CELLS:
        cell = f"C{int(capacity)}-R{str(regen).replace('.', 'p')}"
        table[cell] = {}
        for metric in METRICS:
            by_level = {
                identity: [s[f"mean_{metric}"] for s in summaries
                           if (s["capacity"], s["regen_rate"], s["identity_feedback_strength"])
                           == (capacity, regen, identity)]
                for identity in IDENTITY_LEVELS
            }
            low, high = by_level[0.0], by_level[0.5]
            diffs = [b - a for a, b in zip(low, high)]  # same seed order in both levels
            table[cell][metric] = {
                "identity_0p0": statistics.fmean(low), "identity_0p5": statistics.fmean(high),
                "paired_difference": statistics.fmean(diffs),
                "share_of_seeds_with_positive_difference": sum(d > 0 for d in diffs) / len(diffs),
            }
    result = {"description": __doc__.strip().splitlines()[0], "exploratory": True,
              "runs_matched_against_original": checked, "analysis_window": args.window,
              "seed_start": args.seed_start, "seeds_per_cell": args.seeds_per_cell, "cells": table}
    with open(os.path.join(args.out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)

    print(f"\n{checked} runs matched the original seed summaries.")
    for cell, metrics in table.items():
        print(f"\n{cell}")
        for metric, v in metrics.items():
            print(f"  {metric:28s} {v['identity_0p0']:8.4f} -> {v['identity_0p5']:8.4f}  "
                  f"diff {v['paired_difference']:+.4f}  "
                  f"(+ in {v['share_of_seeds_with_positive_difference']:.0%} of seeds)")


if __name__ == "__main__":
    main()
