"""Pilot-only search for a sustained intermediate resource-scarcity regime.

This routine ranks candidate resource settings using scarcity metrics only.
Cooperation/conflict are reported as exploratory diagnostics and MUST NOT be
used to choose the regime. Calibration seeds should not be reused for the final
hypothesis analysis.
"""
from __future__ import annotations

import copy
import statistics
from typing import Iterable

from ..simulation.engine import Simulation


def _mean(values):
    return statistics.fmean(values) if values else 0.0


def evaluate_regime_candidates(
    base_config,
    capacities: Iterable[float],
    regen_rates: Iterable[float],
    n_runs: int = 4,
    seed_start: int = 10_000,
    analysis_window: int = 100,
    scarcity_target: tuple[float, float] = (0.30, 0.60),
    ceiling_threshold: float = 0.98,
    max_ceiling_fraction: float = 0.10,
):
    """Run a small factorial pilot and rank regimes by the predeclared target.

    Each candidate cell receives a disjoint seed block, avoiding the mistaken
    assumption that the shared simulation RNG remains aligned across changed
    trajectories. Initial stock/capacity ratio is held equal to the base config.
    """
    if n_runs < 2:
        raise ValueError("n_runs must be at least 2 to estimate between-seed variation")
    if analysis_window <= 0 or analysis_window > base_config.n_ticks:
        raise ValueError("analysis_window must be in 1..base_config.n_ticks")
    low, high = scarcity_target
    if not (0 <= low < high <= 1):
        raise ValueError("scarcity_target must satisfy 0 <= low < high <= 1")

    initial_food_fraction = base_config.initial_food_per_agent / base_config.resource_capacity_per_agent
    initial_water_fraction = base_config.initial_water_per_agent / base_config.resource_capacity_per_agent
    candidates = []
    cell_index = 0

    for capacity in capacities:
        if capacity <= 0:
            raise ValueError("resource capacities must be positive")
        for regen in regen_rates:
            if not 0 <= regen <= 1:
                raise ValueError("regen rates must be in [0, 1]")
            seed_values = list(range(seed_start + cell_index * n_runs,
                                     seed_start + (cell_index + 1) * n_runs))
            cell_index += 1
            run_summaries = []
            all_window_scarcity = []

            for seed in seed_values:
                config = copy.deepcopy(base_config)
                config.seed = seed
                config.resource_capacity_per_agent = float(capacity)
                config.initial_food_per_agent = float(capacity) * initial_food_fraction
                config.initial_water_per_agent = float(capacity) * initial_water_fraction
                config.food_regen_rate = float(regen)
                config.water_regen_rate = float(regen)

                rows = Simulation(config).run().to_rows()
                tail = rows[-analysis_window:]
                scarcity = [float(row["true_scarcity"]) for row in tail]
                all_window_scarcity.extend(scarcity)
                run_summaries.append({
                    "seed": seed,
                    "mean_true_scarcity": _mean(scarcity),
                    "mean_cooperation_rate": _mean([float(row["cooperation_rate"]) for row in tail]),
                    "mean_conflict_rate": _mean([float(row["conflict_rate"]) for row in tail]),
                    "mean_population": _mean([float(row["population"]) for row in tail]),
                    "final_population": int(rows[-1]["population"]),
                })

            scarcity_by_seed = [r["mean_true_scarcity"] for r in run_summaries]
            mean_scarcity = _mean(scarcity_by_seed)
            seeds_within_target = [low <= value <= high for value in scarcity_by_seed]
            seed_target_fraction = sum(seeds_within_target) / len(seeds_within_target)
            ceiling_fraction = sum(x >= ceiling_threshold for x in all_window_scarcity) / len(all_window_scarcity)
            in_target = low <= mean_scarcity <= high
            ceiling_ok = ceiling_fraction <= max_ceiling_fraction
            candidates.append({
                "resource_capacity_per_agent": float(capacity),
                "food_regen_rate": float(regen),
                "water_regen_rate": float(regen),
                "initial_food_per_agent": float(capacity) * initial_food_fraction,
                "initial_water_per_agent": float(capacity) * initial_water_fraction,
                "seeds": seed_values,
                "n_runs": n_runs,
                "analysis_window": analysis_window,
                "mean_true_scarcity": mean_scarcity,
                "sd_true_scarcity_between_seeds": statistics.stdev(scarcity_by_seed),
                "n_seed_means_within_scarcity_target": sum(seeds_within_target),
                "fraction_seed_means_within_scarcity_target": seed_target_fraction,
                "fraction_window_at_or_above_ceiling_threshold": ceiling_fraction,
                "mean_cooperation_rate_exploratory": _mean([r["mean_cooperation_rate"] for r in run_summaries]),
                "mean_conflict_rate_exploratory": _mean([r["mean_conflict_rate"] for r in run_summaries]),
                "mean_population": _mean([r["mean_population"] for r in run_summaries]),
                "seed_summaries": run_summaries,
                "within_scarcity_target": in_target,
                "ceiling_fraction_acceptable": ceiling_ok,
                "eligible_for_followup_pilot": in_target and ceiling_ok,
                "distance_from_target_midpoint": abs(mean_scarcity - (low + high) / 2),
            })

    candidates.sort(key=lambda row: (
        not row["eligible_for_followup_pilot"],
        row["distance_from_target_midpoint"],
        row["sd_true_scarcity_between_seeds"],
    ))
    for rank, row in enumerate(candidates, start=1):
        row["scarcity_only_rank"] = rank
    return candidates
