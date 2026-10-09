"""TASK-502: a lightweight causal-NARRATIVE extractor (doc 1, section 13's
"WHY did society collapse?"). This is explicitly NOT a causal-inference
engine — it reports the ORDER in which known warning signs first crossed
their thresholds in one particular run. Order-of-occurrence is not proof of
causation (PROJECT_CONSTITUTION rule 4: document assumptions/limitations),
but it is the honest, cheap thing this project can offer, and it is what a
human reviewing a collapsed run would look at first.
"""
from typing import List

# (metric key, comparison, threshold, human-readable label)
# "population_below_founders" is handled specially (needs founder_population).
# Leadership is NOT in this list — it needs its own transition logic, see below
# (ISSUE-008: "never formed" and "lost after forming" are different stories).
DEFAULT_SIGNS = [
    ("true_scarcity", ">", 0.7, "kaynaklar ciddi şekilde tükendi (true_scarcity > 0.7)"),
    ("avg_stress", ">", 0.7, "ortalama stres yüksek seviyeye çıktı (avg_stress > 0.7)"),
    ("conflict_rate", ">", 0.3, "çatışma oranı yükseldi (conflict_rate > 0.3)"),
    ("avg_trust", "<", 0.0, "ortalama güven negatife döndü (avg_trust < 0)"),
    ("population_below_founders", "special", None, "nüfus kurucu sayısının altına düştü"),
]


def extract_narrative(rows: List[dict], founder_population: int) -> List[str]:
    """Walk the run tick by tick; for each warning sign, record the FIRST
    tick it was triggered; report all triggered signs in the order they
    actually happened.

    ISSUE-008 fix: leadership used to be reported as "has_leader == 0", which
    fired at tick 1 whenever no leader had formed YET — indistinguishable from
    an institution that formed and then collapsed. Now a genuine 1->0
    transition is reported as "kayboldu" (lost), and a leader that never forms
    at all is reported separately as an informational note, not a warning sign.
    """
    crossed = {}
    leader_ever_formed = False
    leader_lost_tick = None
    for row in rows:
        if row.get("has_leader") == 1:
            leader_ever_formed = True
        elif leader_ever_formed and row.get("has_leader") == 0 and leader_lost_tick is None:
            leader_lost_tick = row["tick"]

        for key, op, value, label in DEFAULT_SIGNS:
            if key in crossed:
                continue
            if key == "population_below_founders":
                if "population" not in row:
                    continue
                triggered = row["population"] < founder_population
            else:
                if key not in row:
                    continue
                v = row[key]
                triggered = (v > value) if op == ">" else (v < value) if op == "<" else (v == value)
            if triggered:
                crossed[key] = (row["tick"], label)

    if leader_lost_tick is not None:
        crossed["leadership_lost"] = (leader_lost_tick, "liderlik kurumu oluşmuştu ama kayboldu")
    elif not leader_ever_formed:
        last_tick = rows[-1]["tick"] if rows else 0
        crossed["leadership_never_formed"] = (last_tick, "liderlik hiç oluşmadı (bilgilendirici not, uyarı değil)")

    ordered = sorted(crossed.values(), key=lambda pair: pair[0])
    return [f"tick {tick}: {label}" for tick, label in ordered]
