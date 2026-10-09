"""Entry point: run a baseline V0 simulation, save metrics.csv + metrics.png."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation
from ship_of_fools.visualization.plots import plot_timeseries


def main():
    config = Config()
    sim = Simulation(config)
    metrics = sim.run()
    rows = metrics.to_rows()

    os.makedirs("output", exist_ok=True)
    with open("output/metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[-1].keys())
        writer.writeheader()
        writer.writerows(rows)

    plot_timeseries(rows, "output/metrics.png")

    last = rows[-1]
    print(f"Simulation complete. {last['population']}/{config.n_agents} agents alive at tick {config.n_ticks}.")
    print(f"Final avg_stress={last.get('avg_stress'):.3f}  avg_trust={last.get('avg_trust'):.3f}  "
          f"inequality_gini={last.get('inequality_gini'):.3f}  avg_foolishness={last.get('avg_foolishness'):.3f}")


if __name__ == "__main__":
    main()
