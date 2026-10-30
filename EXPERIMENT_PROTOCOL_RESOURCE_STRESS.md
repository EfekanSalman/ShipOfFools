# Experiment Protocol: Resource Regime, Cooperation and Conflict

**Status:** the protocol was fixed before the final run; the final run was completed
on 2026-10-04. The calibration/pilot seeds were not included in the final results.
Results are in the separate file [RESOURCE_STRESS_RESULTS.md](RESOURCE_STRESS_RESULTS.md).

## Research question

In the model, how do resource capacity and resource regeneration rates change the
population's scarcity, cooperation and conflict trajectories? How much do the effects
vary between seeds, and do capacity and regeneration influence each other?

This is a **within-model** intervention question. The results are not to be taken as
direct causal claims about real societies.

## Rationale and design

In the first scarcity pilot, the setting `resource_capacity_per_agent=90, regen=0.019`
gave medium scarcity in the first seed group, but in the new 20-seed group the mean
scarcity was 0.853. The `120 / 0.016` condition gave a mean of 0.582 in the new
group; however, only in 11/20 of the seeds was the last-window mean in the 0.30–0.60
band. For this reason we do not choose a single "medium scarcity" parameter and
assume that all seeds will behave similarly. We examine the distribution across
regimes and across seeds together.

2×2 factorial conditions:

| Cell | Capacity/founder | Food and water regen/tick |
|---|---:|---:|
| C90-R016 | 90 | 0.016 |
| C90-R019 | 90 | 0.019 |
| C120-R016 | 120 | 0.016 |
| C120-R019 | 120 | 0.019 |

The initial resource stock is kept at the same fraction of capacity in all cells:
initial food and water are each `2/3 × capacity`. The other parameters stay fixed at
the `Config` defaults. Run: 80 founder agents, 500 ticks.

## Hypotheses

- **H1 — manipulation check:** an increase in capacity or regeneration reduces the
  final-period true scarcity.
- **H2 — behavioral outcome:** more favorable resource conditions increase the
  final-period cooperation measure and reduce the conflict measure.
- **H3 — interaction:** the effect of the regeneration rate may vary by capacity level.

H1, H2 and H3 will be tested as within-model results. If an uncertainty interval
covers zero, the result will not be settled as "no effect"; the estimate and the
uncertainty will be reported.

## Outcome measures

**Primary outcomes:** the mean `cooperation_rate` and `conflict_rate` over each
seed's last 100 ticks.

- `cooperation_rate`: the proportion of living agents whose final action is `share`
  or `socialize`.
- `conflict_rate`: the proportion of living agents whose final action is `steal`.

These are limited operational definitions of the broad concepts "cooperation" and
"conflict"; they should not be interpreted, for example, as trust, amount shared or
violence.

**Manipulation check and secondary outcomes:** `true_scarcity`, `avg_stress`,
`avg_trust`, `inequality_gini`, `population`, `avg_health`. The final-period means
and the full time series for each seed are stored.

Each tick is not counted as an independent observation. A simulation seed is the
experimental unit; the last-100-tick mean is the seed-level summary value. This
avoids an artificial sample size that counts ticks as independent samples.

## Seed and sample plan

- 30 seeds/cell as the initial final sample; 120 simulations in total.
- The final seed range is 30000–30119; each cell is given a disjoint block of 30.
- The pilot seed ranges are 10000–10063 and 20000–20079; they are not used in the
  final analysis.
- It will not be claimed that the same seed was used across conditions. The existing
  simulation's shared RNG stream does not guarantee aligning common shocks once
  behaviors diverge.
- 30 seeds is not a universal guarantee of adequacy. Seed-level estimates and
  uncertainty intervals are reported; if the precision of the results is limited,
  additional seeds are added as a separate, documented extension.

## Analysis

- Cell means, the between-seed standard deviation and the 95% bootstrap confidence
  interval are reported.
- The capacity main effect, the regeneration main effect and the 2×2
  difference-of-differences interaction are computed from the seed-level summaries.
  The seeds of each cell are resampled separately; 10,000 bootstrap draws are made
  with a fixed and recorded analysis seed.
- The primary outcomes are two outcome measures and three factorial contrasts;
  instead of a binary decision by p-value, the estimates and confidence intervals are
  interpreted. Exploratory secondary measures are clearly labeled.
- The full time series are presented for descriptive and dynamic assessment; the
  tick-level rows are not used to inflate the inferential sample size.
- The raw seed summaries, time series, configuration, seed assignment rule, Python
  version and analysis code are stored together.

## Interpretation limits

- In the final factorial study the agents moved in fixed list/ID order and with
  immediate effects. The follow-up comparison with an order shuffled at the start of
  each tick is reported in `SCHEDULE_ROBUSTNESS_RESULTS.md`.
- The feedback among resources, regeneration and stress may be nonlinear; since
  means can hide the seed distribution, all seed results are also reported.
- Since no calibration/validation with human data was done, the results belong to the
  internal dynamics of the ship simulation.

## Implementation

The experiment was run with `run_resource_factorial.py` at the 30 seeds/cell setting.
The raw results are in `output/resource_factorial/`. If a new run is made with a
protocol change, it must not replace this study; it must be recorded with a separate
version and seed range.
