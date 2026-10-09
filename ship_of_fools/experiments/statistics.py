"""Inferential statistics for comparing simulation conditions.

The gap this closes: every earlier comparison in this project (ISSUE-001,
ISSUE-004, ISSUE-007, run_sensitivity.py) reported mean±std across 4-10 seeds
and eyeballed whether values "looked separated". That is not a significance
test. This module adds a real one, and is honest that it does not retroactively
fix any earlier claim — see REVALIDATION.md for which specific findings were
re-checked with it.
"""
import math
import statistics
from typing import List, Tuple

from scipy import stats as scipy_stats  # required; environment has scipy 1.17.1


def confidence_interval(values: List[float], confidence: float = 0.95) -> Tuple[float, float, int]:
    """(mean, half_width, n). Report as mean ± half_width. Uses Student's t
    (not a normal approximation) — correct for the small samples (n<30) used
    throughout this project."""
    n = len(values)
    if n < 2:
        return (values[0] if values else float("nan"), float("nan"), n)
    mean = statistics.mean(values)
    se = statistics.stdev(values) / math.sqrt(n)
    t_crit = scipy_stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)
    return (mean, t_crit * se, n)


def welch_t_test(a: List[float], b: List[float]) -> Tuple[float, float]:
    """Welch's t-test (unequal-variance) rather than Student's: several
    metrics in this model saturate at a boundary under one condition and not
    the other (see KNOWN_ISSUES.md), which breaks the equal-variance
    assumption a plain t-test needs. Returns (t_statistic, p_value), two-sided."""
    t_stat, p_value = scipy_stats.ttest_ind(a, b, equal_var=False)
    return float(t_stat), float(p_value)


def cohens_d(a: List[float], b: List[float]) -> float:
    """Standardized effect size, pooled SD. Rule of thumb: 0.2 small, 0.5
    medium, 0.8 large — statistical significance (p<0.05) does not by itself
    say whether an effect is large enough to matter; report both."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    va, vb = statistics.variance(a), statistics.variance(b)
    pooled_sd = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled_sd == 0:
        return float("nan")
    return (statistics.mean(a) - statistics.mean(b)) / pooled_sd
