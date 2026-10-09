"""Scale test: does the simulation stay usable as n_agents grows?

Doc 1 asks for "100 -> 500 -> 1,000 -> 10,000 agents". This measures actual
wall-clock time per tick at increasing population sizes and fits a rough
power-law exponent (time ~ n^k) to see whether the engine scales linearly
(k~1, fine) or worse (k~2, a real bottleneck — see the code-review hypothesis
in this file's __main__ output).

Kept SHORT on purpose (n_ticks=20): this measures per-tick COST, not
long-run dynamics — comparing metric trajectories across population sizes is
a separate question this script does not answer.
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation

SIZES = [100, 200, 400, 800, 1600]
N_TICKS = 20


def main():
    print(f"{'n_agents':>10s}{'total_s':>12s}{'s_per_tick':>14s}{'s_per_agent_tick':>20s}")
    results = []
    for n in SIZES:
        config = Config(n_agents=n, n_ticks=N_TICKS, birth_rate_base=0.0)  # births off: isolate raw per-tick cost from population growth
        sim = Simulation(config)
        t0 = time.time()
        sim.run()
        elapsed = time.time() - t0
        per_tick = elapsed / N_TICKS
        per_agent_tick = per_tick / n
        results.append((n, elapsed, per_tick, per_agent_tick))
        print(f"{n:10d}{elapsed:12.3f}{per_tick:14.4f}{per_agent_tick:20.6f}")

    # rough power-law fit: log(time_per_tick) = k * log(n) + c
    xs = [math.log(n) for n, _, _, _ in results]
    ys = [math.log(t) for _, _, t, _ in results]
    n = len(xs)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    k = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum((x - mean_x) ** 2 for x in xs)
    print(f"\nFitted scaling exponent: time_per_tick ~ n_agents^{k:.2f}")
    print("(k~1.0 = linear/OK, k~2.0 = quadratic bottleneck)")


if __name__ == "__main__":
    main()
