# REVALIDATION — re-testing earlier findings with formal statistics

This file was generated from the output of `run_revalidation.py`
(`output/revalidation_results.json`); the numbers were not transcribed by hand.
Aim: to put through a real significance test the 4 findings that I had
previously reported as "they look different on inspection".

## Method
- Each condition uses **30 seeds**, with the **same seeds** in both conditions; n_agents=60, 300 ticks.
- Metric = the mean of the last 50 ticks of each run.
- Welch t-test (no equal-variance assumption — some metrics stick to the ceiling
  in one condition), 95% CI (Student t), Cohen d.
- **Multiple comparisons:** 4 comparisons × 5 metrics = 20 tests → Bonferroni threshold
  0.05/20 = **0.0025**.

## Results

### 1. `resource_capacity_per_agent` 75 → 150
Earlier claim: dominant lever (sensitivity sweep + ISSUE-007).

| metric | A (mean ± 95% CI) | B (mean ± 95% CI) | Welch p | Cohen d | After Bonferroni |
|---|---|---|---|---|---|
| true_scarcity | 0.996 ± 0.007 | 0.021 ± 0.006 | 1.4e-80 | -54.98 | **significant** |
| population | 75.369 ± 1.547 | 88.646 ± 1.976 | 3.2e-15 | +2.79 | **significant** |
| avg_trust | -0.034 ± 0.002 | 0.031 ± 0.001 | 2.4e-54 | +15.93 | **significant** |
| inequality_gini | 0.440 ± 0.010 | 0.368 ± 0.009 | 8.2e-16 | -2.86 | **significant** |
| conflict_rate | 0.296 ± 0.004 | 0.159 ± 0.002 | 8.4e-42 | -15.72 | **significant** |

### 2. `identity_feedback_strength` 0.0 → 0.5
Earlier claim: erodes trust, dose-dependent (ISSUE-004, 5 seeds).

| metric | A (mean ± 95% CI) | B (mean ± 95% CI) | Welch p | Cohen d | After Bonferroni |
|---|---|---|---|---|---|
| true_scarcity | 0.987 ± 0.016 | 0.999 ± 0.001 | 0.12 | +0.42 | not significant |
| population | 77.141 ± 1.847 | 72.798 ± 1.276 | 0.00023 | -1.02 | **significant** |
| avg_trust | -0.021 ± 0.001 | -0.041 ± 0.002 | 4.2e-26 | -4.88 | **significant** |
| inequality_gini | 0.370 ± 0.014 | 0.486 ± 0.008 | 7.1e-19 | +3.73 | **significant** |
| conflict_rate | 0.271 ± 0.004 | 0.306 ± 0.004 | 6.8e-19 | +3.37 | **significant** |

### 3. `reconciliation_bonus` 0.0 → 0.35
Earlier claim: improves `avg_trust` (ISSUE-005, **single seed**).

| metric | A (mean ± 95% CI) | B (mean ± 95% CI) | Welch p | Cohen d | After Bonferroni |
|---|---|---|---|---|---|
| true_scarcity | 0.993 ± 0.013 | 0.996 ± 0.007 | 0.64 | +0.12 | not significant |
| population | 74.624 ± 1.788 | 75.369 ± 1.547 | 0.52 | +0.17 | not significant |
| avg_trust | -0.051 ± 0.002 | -0.034 ± 0.002 | 3.9e-22 | +3.98 | **significant** |
| inequality_gini | 0.435 ± 0.012 | 0.440 ± 0.010 | 0.54 | +0.16 | not significant |
| conflict_rate | 0.298 ± 0.004 | 0.296 ± 0.004 | 0.5 | -0.17 | not significant |

### 4. `misinformation_rate` 0.05 → 0.35
Earlier result: no reliable effect, closed (ISSUE-001, 8 seeds).

| metric | A (mean ± 95% CI) | B (mean ± 95% CI) | Welch p | Cohen d | After Bonferroni |
|---|---|---|---|---|---|
| true_scarcity | 0.996 ± 0.007 | 0.999 ± 0.002 | 0.49 | +0.18 | not significant |
| population | 75.369 ± 1.547 | 75.099 ± 1.385 | 0.79 | -0.07 | not significant |
| avg_trust | -0.034 ± 0.002 | -0.034 ± 0.002 | 0.87 | +0.04 | not significant |
| inequality_gini | 0.440 ± 0.010 | 0.443 ± 0.010 | 0.66 | +0.11 | not significant |
| conflict_rate | 0.296 ± 0.004 | 0.299 ± 0.006 | 0.36 | +0.24 | not significant |

### 4b. `misinformation_rate` 0.05 → 0.35, **resource-abundant regime** (`resource_capacity_per_agent=150`)
Why it was run: in the default regime `true_scarcity` sticks to ≈ 1.0 (ceiling effect);
the "no effect" result might have stemmed from that. 6 tests → threshold 0.0083.

| metric | A (mean ± 95% CI) | B (mean ± 95% CI) | Welch p | Cohen d | After Bonferroni |
|---|---|---|---|---|---|
| true_scarcity | 0.021 ± 0.006 | 0.020 ± 0.007 | 0.98 | -0.01 | not significant |
| population | 88.646 ± 1.976 | 88.203 ± 2.104 | 0.75 | -0.08 | not significant |
| avg_trust | 0.031 ± 0.001 | 0.031 ± 0.002 | 0.76 | +0.08 | not significant |
| inequality_gini | 0.368 ± 0.009 | 0.379 ± 0.007 | 0.048 | +0.52 | raw p<0.05, did NOT pass |
| conflict_rate | 0.159 ± 0.002 | 0.159 ± 0.003 | 0.9 | +0.03 | not significant |
| belief_polarization | 0.107 ± 0.001 | 0.106 ± 0.002 | 0.4 | -0.22 | not significant |

## What we can say

| Earlier claim | Status | Note |
|---|---|---|
| Resource capacity is the dominant lever | **Confirmed, very strongly** | Significant in 5 of 5 metrics; effect sizes are enormous (d = −55 … +16). |
| `identity_feedback_strength` erodes trust | **Direction confirmed** (endpoints 0.0 vs 0.5) | `avg_trust`, `conflict_rate`, `inequality_gini`, `population` significant. **Intermediate doses (0.1/0.15/0.3) were not re-tested** → the "monotonic dose-dependence" claim was not re-confirmed. The absolute `avg_trust` values in the old table (0.011 → −0.023) CANNOT BE COMPARED with the new results (−0.021 → −0.041): config, n and ticks changed. |
| The reconciliation mechanic improves `avg_trust` | **Confirmed** (but limited) | The single-seed claim holds at n=30 (−0.051 → −0.034). **However**, it has no effect at all on `population`, `inequality_gini`, `conflict_rate`: it corrects the measured trust, it does not change behavior/the economy. |
| `misinformation_rate` is ineffective | **Confirmed, in two regimes** | There is no significant effect either in the collapse regime or in the resource-abundant regime. In 4b, `inequality_gini` came out at raw p=0.048 but did not pass Bonferroni. Even `belief_polarization` does not change — interesting, since it is the expected channel; the reason was not investigated. |

## Reproducibility verification
The same (default) config + the same seeds in three separate comparisons were run in
mutually independent processes, and the `avg_trust` means are **bit-for-bit identical**
(−0.03396453997424015). PROJECT_CONSTITUTION rule 6 was this time verified by measurement.

## What these results CANNOT do (important)

1. **p-values are weak evidence in simulation.** Significance depends on how many runs
   I choose to make; with enough seeds every systematic difference becomes "significant".
   So the real information is the **effect size and the confidence interval**, not p. p<1e−50
   does not mean "important in the real world", it means "not seed noise within this model".
2. **Values such as Cohen d = −55 are not realistic effect sizes.** The model's
   between-seed variance is artificially very small because of the ceiling sticking;
   d comes out huge. The ordering/sign carries information; the magnitude should not be interpreted.
3. **All of it is about the model itself.** None of it is a claim about real societies;
   `REFERENCES.md` states explicitly that most mechanisms contain no empirical calibration.
4. **A single regime.** Comparisons 1-3 were made only in the collapse regime
   (default config, `true_scarcity` ≈ 1.0). Only `misinformation_rate` was also tested
   in the resource-abundant regime (4b). See `KNOWN_ISSUES.md` ISSUE-011.

## Findings NOT re-validated (still small-sample)
- 19-parameter sensitivity sweep: **4 seeds**, no confidence intervals (`run_sensitivity.py`).
- 2×2 interaction test (`resource_capacity` × `food_regen_rate`): **4 seeds**.
- ISSUE-007 population-collapse rates (100% / 30% / 80%): **10 seeds**, 2000 ticks.
- ISSUE-006 (population falling to 1): **single seed**.
- ISSUE-004 intermediate doses: 5 seeds, old config.
- Scale test: single run/size.
These are tracked in `KNOWN_ISSUES.md` ISSUE-012.
