"""TASK-207: healthcare — health recovery is modulated by institutional
legitimacy. Same pattern as education.py: a small baseline always applies
("the sick get cared for by whoever's around"), and a leader institution's
TRUE legitimacy adds an extra recovery boost on top — no leader, no
institutional bonus, only the informal baseline.
"""


def health_recovery_rate(true_legitimacy: float, baseline_rate: float,
                          institutional_bonus_at_full_legitimacy: float) -> float:
    return baseline_rate + institutional_bonus_at_full_legitimacy * true_legitimacy
