"""Regenerate the interactive HTML dashboard (TASK-701) for any config.

Runs an instrumented simulation (ship_of_fools/visualization/dashboard_export.py),
then splices the resulting JSON bundle into the single-file HTML template.
The output is fully self-contained apart from two pinned CDN scripts
(Chart.js, D3) — open it in any browser, or publish it as an artifact.

Usage:
    python3 run_dashboard.py                      # default: 80 agents, 500 ticks
    python3 run_dashboard.py --agents 120 --ticks 800 --seed 7
    python3 run_dashboard.py --capacity 150       # e.g. the stable-society override from ISSUE-007
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ship_of_fools.configuration.config import Config
from ship_of_fools.visualization.dashboard_export import export_bundle

TEMPLATE = os.path.join(os.path.dirname(__file__), "ship_of_fools", "visualization", "dashboard_template.html")
PLACEHOLDER = "/*__DASHBOARD_DATA__*/"


def build_dashboard(config, out_path: str, sample_size: int = 18, snapshot_interval: int = 10) -> int:
    data = export_bundle(config, sample_size=sample_size, snapshot_interval=snapshot_interval)
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    assert PLACEHOLDER in template, "template is missing the data placeholder"
    html = template.replace(PLACEHOLDER, data)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return len(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", type=int, default=80)
    ap.add_argument("--ticks", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--capacity", type=float, default=None, help="resource_capacity_per_agent override")
    ap.add_argument("--out", default="output/dashboard.html")
    args = ap.parse_args()

    overrides = {}
    if args.capacity is not None:
        overrides["resource_capacity_per_agent"] = args.capacity
        overrides["initial_food_per_agent"] = args.capacity * (50.0 / 75.0)
        overrides["initial_water_per_agent"] = args.capacity * (50.0 / 75.0)
    config = Config(n_agents=args.agents, n_ticks=args.ticks, seed=args.seed, **overrides)

    size = build_dashboard(config, args.out)
    print(f"Dashboard written to {args.out} ({size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
