"""Structural and aggregate measurements that doc 1 §12 asked for and the
tracker did not have: polarization, network centralization, cohesion,
mobility. Pure functions, no dependency on the simulation classes.

DESIGN RULES
- Measuring must never change what is measured. Nothing here touches the
  simulation's RNG (callers pass their own `random.Random` for sampling).
- Where a quantity cannot be defined yet, return NaN instead of a plausible
  looking default (a fake 0.0 would read as "no inequality/mobility").
- What is deliberately NOT measured: "innovation". The model has no
  technology or idea-generation mechanism, so any innovation number would be
  invented. `human_capital_total` (summed forage skill) is reported instead
  and is documented as a skill-accumulation proxy only.

Definitions and sources (see REFERENCES.md for verification status):
- Polarization: Esteban & Ray (1994), Econometrica 62(4):819-851, with the
  binned form and alpha=1.6. Normalized so that two equal masses at the
  two extremes of the range score 1.0 and a single mass scores 0.0.
- Centralization: Freeman's in-degree centralization (Freeman 1978/79,
  Social Networks 1(3)), normalized by the star-graph maximum (n-1)^2.
- Clustering: Watts & Strogatz (1998), average local clustering over nodes
  with at least two neighbours.
"""
import math
import random
from typing import Dict, List, Sequence, Set

NAN = float("nan")


def esteban_ray_polarization(values: Sequence[float], bins: int = 10, alpha: float = 1.6,
                              lo: float = 0.0, hi: float = 1.0) -> float:
    n = len(values)
    if n == 0 or bins < 2 or hi <= lo:
        return 0.0
    counts = [0] * bins
    span = hi - lo
    for v in values:
        v = min(hi, max(lo, v))
        idx = min(bins - 1, int((v - lo) / span * bins))
        counts[idx] += 1
    pi = [c / n for c in counts]
    pos = [i / (bins - 1) for i in range(bins)]
    total = 0.0
    for i in range(bins):
        if pi[i] == 0.0:
            continue
        weight_i = pi[i] ** (1.0 + alpha)
        for j in range(bins):
            if i != j and pi[j] > 0.0:
                total += weight_i * pi[j] * abs(pos[i] - pos[j])
    pmax = 2.0 * 0.5 ** (2.0 + alpha)  # two equal masses at the range extremes
    return total / pmax


def positive_adjacency(trust: Dict[int, Dict[int, float]], alive: Set[int],
                        threshold: float = 0.05) -> Dict[int, Set[int]]:
    """Directed positive-trust edges a -> b among living agents."""
    out = {}
    for a in alive:
        out[a] = {b for b, t in trust.get(a, {}).items() if t > threshold and b in alive}
    return out


def in_degree_centralization(pos_out: Dict[int, Set[int]]) -> float:
    n = len(pos_out)
    if n < 3:
        return 0.0
    indeg = {a: 0 for a in pos_out}
    for targets in pos_out.values():
        for b in targets:
            indeg[b] += 1
    dmax = max(indeg.values())
    return sum(dmax - d for d in indeg.values()) / float((n - 1) ** 2)


def cohesion_metrics(pos_out: Dict[int, Set[int]], rng: random.Random,
                      sample: int = 300) -> Dict[str, float]:
    """Reciprocity, clustering and giant-component share of the positive-trust graph."""
    nodes = sorted(pos_out)
    n = len(nodes)
    n_edges = sum(len(s) for s in pos_out.values())
    if n == 0:
        return {"pos_reciprocity": 0.0, "pos_clustering": 0.0, "giant_component_frac": 0.0}

    und: Dict[int, Set[int]] = {a: set() for a in nodes}
    mutual = 0
    for a, targets in pos_out.items():
        for b in targets:
            und[a].add(b)
            und[b].add(a)
            if a in pos_out.get(b, ()):
                mutual += 1
    reciprocity = mutual / n_edges if n_edges else 0.0

    pool = nodes if n <= sample else rng.sample(nodes, sample)
    coeffs = []
    for a in pool:
        nb = und[a]
        k = len(nb)
        if k < 2:
            continue
        links = sum(len(und[x] & nb) for x in nb)  # every link counted twice
        coeffs.append(links / float(k * (k - 1)))
    clustering = sum(coeffs) / len(coeffs) if coeffs else 0.0

    parent = {a: a for a in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a in nodes:
        for b in und[a]:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    sizes: Dict[int, int] = {}
    for a in nodes:
        r = find(a)
        sizes[r] = sizes.get(r, 0) + 1
    return {"pos_reciprocity": reciprocity, "pos_clustering": clustering,
            "giant_component_frac": max(sizes.values()) / n}


def _ranks(values: Sequence[float]) -> List[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    n = len(x)
    if n != len(y) or n < 3:
        return NAN
    rx, ry = _ranks(x), _ranks(y)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0.0 or vy == 0.0:
        return NAN
    return cov / math.sqrt(vx * vy)


def wealth_rank_persistence(prev: Dict[int, float], cur: Dict[int, float]) -> float:
    """Spearman correlation of wealth between two moments, over agents alive
    at both. 1.0 = frozen hierarchy, ~0 = ranks fully reshuffled, <0 = inverted.
    Intragenerational only: newborns have no earlier rank."""
    common = sorted(set(prev) & set(cur))
    if len(common) < 5:
        return NAN
    return spearman([prev[i] for i in common], [cur[i] for i in common])
