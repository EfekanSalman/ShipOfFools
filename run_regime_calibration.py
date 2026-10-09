"""Pilot search for resource settings with sustained intermediate scarcity.

Calibration/pilot seeds are disjoint blocks by candidate and must not be reused
for the final hypothesis analysis.
"""
import argparse
import json
import os
import platform
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.regime_calibration import evaluate_regime_candidates


def _parse_numbers(raw, cast=float):
    try:
        return [cast(piece.strip()) for piece in raw.split(",") if piece.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid comma-separated values: {raw}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=80)
    parser.add_argument("--ticks", type=int, default=400)
    parser.add_argument("--seeds-per-cell", type=int, default=4)
    parser.add_argument("--seed-start", type=int, default=10000)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--capacities", default="75,90,105,120",
                        help="comma-separated resource_capacity_per_agent candidates")
    parser.add_argument("--regen-rates", default="0.010,0.013,0.016,0.019",
                        help="comma-separated rate candidates; applied equally to food and water")
    parser.add_argument("--target-low", type=float, default=0.30)
    parser.add_argument("--target-high", type=float, default=0.60)
    parser.add_argument("--ceiling-threshold", type=float, default=0.98)
    parser.add_argument("--max-ceiling-fraction", type=float, default=0.10)
    parser.add_argument("--out", default="output/regime_calibration_pilot.json")
    args = parser.parse_args()

    if args.agents <= 1 or args.ticks <= 0:
        parser.error("--agents must be >1 and --ticks must be positive")
    if args.seeds_per_cell < 2:
        parser.error("--seeds-per-cell must be >=2")

    capacities = _parse_numbers(args.capacities)
    regen_rates = _parse_numbers(args.regen_rates)
    if not capacities or not regen_rates:
        parser.error("--capacities and --regen-rates must each contain values")

    base = Config(n_agents=args.agents, n_ticks=args.ticks, seed=0)
    results = evaluate_regime_candidates(
        base,
        capacities=capacities,
        regen_rates=regen_rates,
        n_runs=args.seeds_per_cell,
        seed_start=args.seed_start,
        analysis_window=args.window,
        scarcity_target=(args.target_low, args.target_high),
        ceiling_threshold=args.ceiling_threshold,
        max_ceiling_fraction=args.max_ceiling_fraction,
    )

    payload = {
        "experiment": "resource_regime_calibration_pilot",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "n_agents": args.agents,
        "n_ticks": args.ticks,
        "analysis_window": args.window,
        "seeds_per_candidate": args.seeds_per_cell,
        "seed_assignment": "disjoint sequential seed blocks per candidate cell",
        "candidate_seed_start": args.seed_start,
        "candidate_seed_end_inclusive": args.seed_start + len(capacities) * len(regen_rates) * args.seeds_per_cell - 1,
        "scarcity_target": [args.target_low, args.target_high],
        "ceiling_threshold": args.ceiling_threshold,
        "max_ceiling_fraction": args.max_ceiling_fraction,
        "selection_rule": "rank by mean scarcity target and ceiling fraction; per-seed target fraction is diagnostic; cooperation/conflict are exploratory outputs",
        "candidates": results,
    }
    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, allow_nan=False)

    print("Rank | Capacity | Regen | Mean scarcity +/- between-seed SD | Seeds in target | Ceiling share | Coop* | Conflict* | Eligible")
    for row in results:
        print(f"{row['scarcity_only_rank']:>4} | {row['resource_capacity_per_agent']:>8.1f} | "
              f"{row['food_regen_rate']:.3f} | "
              f"{row['mean_true_scarcity']:.3f} +/- {row['sd_true_scarcity_between_seeds']:.3f} | "
              f"{row['n_seed_means_within_scarcity_target']}/{row['n_runs']} | "
              f"{row['fraction_window_at_or_above_ceiling_threshold']:.1%} | "
              f"{row['mean_cooperation_rate_exploratory']:.3f} | "
              f"{row['mean_conflict_rate_exploratory']:.3f} | "
              f"{row['eligible_for_followup_pilot']}")
    eligible = [row for row in results if row["eligible_for_followup_pilot"]]
    if eligible:
        print("\nTop scarcity-only candidate for a follow-up pilot:",
              eligible[0]["resource_capacity_per_agent"],
              eligible[0]["food_regen_rate"])
        print("This is a pilot candidate, not a final calibrated setting.")
    else:
        print("\nNo candidate met the predeclared scarcity/ceiling criteria; expand or revise the grid before choosing a regime.")
    print(f"\nSaved full pilot output: {out_path}")
    print("* Cooperation/conflict are exploratory only and do not affect the ranking.")


if __name__ == "__main__":
    main()
