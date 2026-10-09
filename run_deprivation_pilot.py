"""Pilot: find a regeneration level at which agents are actually deprived (ISSUE-015).

Calibration only. The selection rule below looks at need levels and
population, never at cooperation or conflict outcomes, and these seeds are not
reused in any final experiment.

Selection rule (fixed before running): among the scanned regeneration rates,
pick the highest one at which, for BOTH capacity levels, the seed-mean
need_deficit_rate over the final window is at least 0.20 and every pilot seed
ends with at least 20 living agents.
"""
import argparse
import json
import os
import platform
import statistics
import sys
from dataclasses import asdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


CAPACITIES = (90.0, 120.0)
REGEN_RATES = (0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010, 0.012, 0.016)
METRICS = ("need_deficit_rate", "avg_min_need", "true_scarcity", "population", "avg_stress")
MIN_DEFICIT = 0.20
MIN_FINAL_POPULATION = 20


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=500)
    parser.add_argument("--seeds-per-cell", type=int, default=4)
    parser.add_argument("--seed-start", type=int, default=91000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--out", default="output/deprivation_pilot.json")
    parser.add_argument("--order", default="fixed", choices=("fixed", "shuffled"), help="agent_update_order")
    args = parser.parse_args()

    base = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0, agent_update_order=args.order)
    cells = []
    seed = args.seed_start
    for capacity in CAPACITIES:
        for regen in REGEN_RATES:
            runs = []
            for _ in range(args.seeds_per_cell):
                cfg = Config(**asdict(base))
                cfg.seed = seed
                cfg.resource_capacity_per_agent = capacity
                cfg.initial_food_per_agent = capacity * (2.0 / 3.0)
                cfg.initial_water_per_agent = capacity * (2.0 / 3.0)
                cfg.food_regen_rate = regen
                cfg.water_regen_rate = regen
                rows = Simulation(cfg).run().to_rows()
                tail = [r for r in rows[-args.window:] if r["population"] > 0]
                run = {"seed": seed, "final_population": int(rows[-1]["population"]),
                       "cumulative_deaths_starvation": rows[-1].get("cumulative_deaths_starvation", 0)}
                for metric in METRICS:
                    run[f"mean_{metric}"] = statistics.fmean(r[metric] for r in tail) if tail else float("nan")
                runs.append(run)
                seed += 1
            cell = {"capacity": capacity, "regen_rate": regen, "runs": runs,
                    "min_final_population": min(r["final_population"] for r in runs)}
            for metric in METRICS:
                cell[f"mean_{metric}"] = statistics.fmean(r[f"mean_{metric}"] for r in runs)
            cell["mean_deaths_starvation"] = statistics.fmean(r["cumulative_deaths_starvation"] for r in runs)
            cells.append(cell)
            print(f"C{int(capacity)} R{regen:.3f}  deficit {cell['mean_need_deficit_rate']:.3f}  "
                  f"min_need {cell['mean_avg_min_need']:.3f}  scarcity {cell['mean_true_scarcity']:.3f}  "
                  f"pop {cell['mean_population']:.1f} (min final {cell['min_final_population']})  "
                  f"starved {cell['mean_deaths_starvation']:.1f}", flush=True)

    def qualifies(regen):
        mine = [c for c in cells if c["regen_rate"] == regen]
        return all(c["mean_need_deficit_rate"] >= MIN_DEFICIT
                   and c["min_final_population"] >= MIN_FINAL_POPULATION for c in mine)

    qualifying = [regen for regen in REGEN_RATES if qualifies(regen)]
    selected = max(qualifying) if qualifying else None
    result = {
        "purpose": "calibration pilot for a deprivation regime; seeds not reused in final experiments",
        "created_utc": datetime.now(timezone.utc).isoformat(), "python_version": platform.python_version(),
        "base_config": asdict(base), "capacities": list(CAPACITIES), "regen_rates": list(REGEN_RATES),
        "seeds_per_cell": args.seeds_per_cell, "seed_start": args.seed_start, "seed_end_inclusive": seed - 1,
        "analysis_window": args.window,
        "selection_rule": {"min_mean_need_deficit_rate": MIN_DEFICIT,
                           "min_final_population_every_seed": MIN_FINAL_POPULATION,
                           "pick": "highest qualifying regen rate, both capacities"},
        "qualifying_regen_rates": qualifying, "selected_regen_rate": selected, "cells": cells,
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    print(f"\nQualifying regen rates: {qualifying}; selected: {selected}")


if __name__ == "__main__":
    main()
