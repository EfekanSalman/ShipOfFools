"""TASK-701: data export for the interactive HTML dashboard.

The core Simulation loop only records population-level aggregates each tick
(metrics/tracker.py) — no per-agent history. Rather than bloating the core
engine with per-agent logging every tick (expensive, mostly unused), this
module runs its OWN instrumented loop: it calls Simulation.step() directly
and snapshots a SAMPLE of founder agents every `snapshot_interval` ticks, plus
a final-tick social network graph. Kept as a separate module so the core
simulation stays lean (ARCHITECTURE.md's "add a module, don't rewrite" rule).
"""
import json
import math
import random
from typing import Dict, List

from ..simulation.engine import Simulation


def run_with_snapshots(config, sample_size: int = 18, snapshot_interval: int = 10):
    sim = Simulation(config)
    founder_ids = list(sim.agent_ids)
    rng_local = random.Random(config.seed + 999)
    sample_ids = set(rng_local.sample(founder_ids, min(sample_size, len(founder_ids))))
    snapshots: Dict[int, List[dict]] = {aid: [] for aid in sample_ids}

    for _ in range(config.n_ticks):
        sim.step()
        if sim.ship.tick % snapshot_interval == 0:
            by_id = {a.id: a for a in sim.agents}
            for aid in sample_ids:
                a = by_id.get(aid)
                if a is None or not a.alive:
                    continue
                p = a.personality
                snapshots[aid].append({
                    "tick": sim.ship.tick, "stress": round(a.stress, 3), "mood": round(a.mood, 3),
                    "health": round(a.health, 3), "wealth": round(a.wealth, 2), "age": a.age_years,
                    "scarcity_belief": round(a.beliefs.scarcity_belief, 3),
                    "institution_trust": round(a.beliefs.institution_trust, 3),
                    "reflected_self": round(a.mental_model.reflected_self, 3),
                    "identity": a.identity.label, "forage_skill": round(a.forage_skill, 3),
                    "personality": {k: round(getattr(p, k), 3) for k in
                                    ("openness", "conscientiousness", "risk_tolerance",
                                     "empathy", "dominance", "conformity", "curiosity")},
                })
    return sim, snapshots


def export_network(sim, max_nodes: int = 90) -> dict:
    """Final-tick trust graph, capped to the most-connected agents for legibility."""
    alive = [a for a in sim.agents if a.alive]
    degree = {a.id: len(sim.social.trust.get(a.id, {})) for a in alive}
    top_ids = sorted(degree, key=lambda i: -degree[i])[:max_nodes]
    top_set = set(top_ids)
    by_id = {a.id: a for a in alive}

    nodes = [{"id": i, "identity": by_id[i].identity.label or "none",
              "stress": round(by_id[i].stress, 2)} for i in top_ids]
    edges = []
    for a_id in top_ids:
        for b_id, trust in sim.social.trust.get(a_id, {}).items():
            if b_id in top_set and abs(trust) > 0.1:
                edges.append({"source": a_id, "target": b_id, "trust": round(trust, 3)})
    return {"nodes": nodes, "edges": edges}


def _nan_to_none(obj):
    """json.dumps writes float('nan') as the bare token NaN, which is NOT valid
    JSON (strict parsers reject it). Some metrics are legitimately undefined
    early in a run (e.g. wealth_rank_mobility before its first window closes),
    so map NaN -> null. The dashboard treats null as a gap in the line."""
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: _nan_to_none(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_nan_to_none(v) for v in obj]
    return obj


def export_bundle(config, sample_size: int = 18, snapshot_interval: int = 10) -> str:
    sim, snapshots = run_with_snapshots(config, sample_size, snapshot_interval)
    bundle = {
        "meta": {"n_agents": config.n_agents, "n_ticks": config.n_ticks, "seed": config.seed},
        "timeseries": sim.metrics.to_rows(),
        "agents": {str(k): v for k, v in snapshots.items()},
        "network": export_network(sim),
    }
    return json.dumps(_nan_to_none(bundle), separators=(",", ":"), allow_nan=False)
