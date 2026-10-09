"""Demo experiment: baseline vs +misinformation (doc 1, Experiment A)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.experiments.runner import run_experiment, summarize_window


def main():
    base = Config(n_agents=60, n_ticks=300)

    baseline = run_experiment(base, overrides={}, n_runs=8)
    high_misinfo = run_experiment(base, overrides={"misinformation_rate": 0.35}, n_runs=8)

    print("=== Baseline (misinformation_rate=%.2f), avg of last 50 ticks ===" % base.misinformation_rate)
    for k, (m, s) in summarize_window(baseline, window=50).items():
        print(f"  {k:26s} mean={m:.3f}  std={s:.3f}")

    print("\n=== High misinformation (misinformation_rate=0.35), avg of last 50 ticks ===")
    for k, (m, s) in summarize_window(high_misinfo, window=50).items():
        print(f"  {k:26s} mean={m:.3f}  std={s:.3f}")


if __name__ == "__main__":
    main()
