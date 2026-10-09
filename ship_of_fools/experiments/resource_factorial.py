"""Pre-specified 2x2 resource experiment with seed-level uncertainty.

Each simulation seed is one experimental unit. Tick observations are summarized
within seed and are never treated as independent replicates.
"""
from __future__ import annotations

import copy
import random
import statistics
from typing import Callable, Iterable

from ..simulation.engine import Simulation


ANALYSIS_METRICS = (
    "cooperation_rate",
    "conflict_rate",
    "true_scarcity",
    "avg_stress",
    "avg_trust",
    "inequality_gini",
    "population",
    "avg_health",
)


def _percentile(sorted_values, probability):
    if not sorted_values:
        return float("nan")
    position = (len(sorted_values) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def _mean_ci(values, draws, rng):
    means = []
    n = len(values)
    for _ in range(draws):
        means.append(statistics.fmean(values[rng.randrange(n)] for _ in range(n)))
    means.sort()
    return [_percentile(means, 0.025), _percentile(means, 0.975)]


def _level_label(value):
    return format(float(value), ".17g").replace(".", "p").replace("-", "m")


def _cell_id(capacity, regen):
    return f"C{_level_label(capacity)}-R{_level_label(regen)}"


def _factorial_contrasts(cell_means, capacities=(90.0, 120.0), regen_rates=(0.016, 0.019)):
    """Return 2x2 high-minus-low main effects and difference-in-differences."""
    low_capacity, high_capacity = sorted(capacities)
    low_regen, high_regen = sorted(regen_rates)
    c_low_low = cell_means[_cell_id(low_capacity, low_regen)]
    c_low_high = cell_means[_cell_id(low_capacity, high_regen)]
    c_high_low = cell_means[_cell_id(high_capacity, low_regen)]
    c_high_high = cell_means[_cell_id(high_capacity, high_regen)]
    return {
        "capacity_high_minus_low": ((c_high_low + c_high_high) / 2.0) - ((c_low_low + c_low_high) / 2.0),
        "regen_high_minus_low": ((c_low_high + c_high_high) / 2.0) - ((c_low_low + c_high_low) / 2.0),
        "capacity_by_regen_interaction": (c_high_high - c_high_low) - (c_low_high - c_low_low),
    }


def run_resource_factorial(
    base_config,
    capacities: Iterable[float] = (90.0, 120.0),
    regen_rates: Iterable[float] = (0.016, 0.019),
    n_runs: int = 30,
    seed_start: int = 30_000,
    analysis_window: int = 100,
    bootstrap_draws: int = 10_000,
    analysis_seed: int = 61_020_26,
    on_run_complete: Callable | None = None,
):
    """Run the pre-specified 2x2 resource design and bootstrap seed-level means.

    Candidate cells receive disjoint seed blocks. The callback, if given, is
    called as ``callback(cell_id, capacity, regen, seed, rows)`` after each run,
    allowing raw per-tick data to be streamed to disk without retaining all
    trajectories in memory.
    """
    capacities = tuple(float(x) for x in capacities)
    regen_rates = tuple(float(x) for x in regen_rates)
    if len(capacities) != 2 or len(set(capacities)) != 2:
        raise ValueError("exactly two distinct capacity levels are required")
    if len(regen_rates) != 2 or len(set(regen_rates)) != 2:
        raise ValueError("exactly two distinct regen levels are required")
    if any(x <= 0 for x in capacities):
        raise ValueError("capacity levels must be positive")
    if any(not 0 <= x <= 1 for x in regen_rates):
        raise ValueError("regen rates must be in [0, 1]")
    if n_runs < 2:
        raise ValueError("n_runs must be at least 2")
    if base_config.resource_capacity_per_agent <= 0:
        raise ValueError("base resource capacity must be positive")
    if not 0 < analysis_window <= base_config.n_ticks:
        raise ValueError("analysis_window must be in 1..base_config.n_ticks")
    if bootstrap_draws < 1000:
        raise ValueError("use at least 1000 bootstrap draws")

    food_fraction = base_config.initial_food_per_agent / base_config.resource_capacity_per_agent
    water_fraction = base_config.initial_water_per_agent / base_config.resource_capacity_per_agent
    cells = {}
    seed_counter = 0

    for capacity in sorted(capacities):
        for regen in sorted(regen_rates):
            cell_id = _cell_id(capacity, regen)
            seeds = range(seed_start + seed_counter * n_runs,
                          seed_start + (seed_counter + 1) * n_runs)
            seed_counter += 1
            cells[cell_id] = {
                "capacity": capacity,
                "regen": regen,
                "seeds": [],
                "seed_summaries": [],
            }

            for seed in seeds:
                config = copy.deepcopy(base_config)
                config.seed = seed
                config.resource_capacity_per_agent = capacity
                config.initial_food_per_agent = capacity * food_fraction
                config.initial_water_per_agent = capacity * water_fraction
                config.food_regen_rate = regen
                config.water_regen_rate = regen
                rows = Simulation(config).run().to_rows()
                tail = rows[-analysis_window:]
                summary = {
                    "seed": seed,
                    "cell": cell_id,
                    "capacity": capacity,
                    "regen_rate": regen,
                    "final_population": int(rows[-1]["population"]),
                }
                for metric in ANALYSIS_METRICS:
                    summary[f"mean_{metric}"] = statistics.fmean(float(row[metric]) for row in tail)
                cells[cell_id]["seeds"].append(seed)
                cells[cell_id]["seed_summaries"].append(summary)
                if on_run_complete is not None:
                    on_run_complete(cell_id, capacity, regen, seed, rows)

    rng = random.Random(analysis_seed)
    cell_statistics = {}
    effects = {}
    for metric in ANALYSIS_METRICS:
        cell_values = {
            cell_id: [summary[f"mean_{metric}"] for summary in cell["seed_summaries"]]
            for cell_id, cell in cells.items()
        }
        cell_means = {cell_id: statistics.fmean(values) for cell_id, values in cell_values.items()}
        metric_cells = {}
        bootstrap_cell_means = {}
        for cell_id, values in cell_values.items():
            ci = _mean_ci(values, bootstrap_draws, rng)
            metric_cells[cell_id] = {
                "n_seeds": len(values),
                "mean": cell_means[cell_id],
                "sd_between_seeds": statistics.stdev(values),
                "median": statistics.median(values),
                "bootstrap_ci95": ci,
            }
            samples = []
            n = len(values)
            for _ in range(bootstrap_draws):
                samples.append(statistics.fmean(values[rng.randrange(n)] for _ in range(n)))
            bootstrap_cell_means[cell_id] = samples

        point_effects = _factorial_contrasts(cell_means, capacities, regen_rates)
        effect_draws = {name: [] for name in point_effects}
        for i in range(bootstrap_draws):
            means_i = {cell_id: draws[i] for cell_id, draws in bootstrap_cell_means.items()}
            for name, value in _factorial_contrasts(means_i, capacities, regen_rates).items():
                effect_draws[name].append(value)
        effects[metric] = {}
        for name, point in point_effects.items():
            values = sorted(effect_draws[name])
            effects[metric][name] = {
                "estimate": point,
                "bootstrap_ci95": [_percentile(values, 0.025), _percentile(values, 0.975)],
            }
        cell_statistics[metric] = metric_cells

    return {
        "cells": cells,
        "cell_statistics": cell_statistics,
        "factorial_effects": effects,
        "analysis_metrics": list(ANALYSIS_METRICS),
        "analysis_window": analysis_window,
        "bootstrap_draws": bootstrap_draws,
        "analysis_seed": analysis_seed,
    }
