# Resource Regime Experiment — Results

## Status and level of interpretation

**Final run completed: 2026-10-04.** This is the within-simulation result of the
pre-specified 2×2 resource regime experiment; it is not a calibration to real
society data or an empirical validation.

## Method

- 80 founder agents, 500 ticks; apart from the `Config` defaults, capacity and the
  food / water regeneration rates were changed.
- Capacity 90/120; food and water regeneration rate together 0.016/0.019.
- The initial food and water stock was 2/3 of capacity in every condition.
- 30 seeds/cell, 4 cells, 120 simulations in total. Seed range 30000–30119;
  the cell seed blocks are disjoint. The conditions are not a matched-seed design.
- The last 100 ticks were averaged within each seed. The seed is the simulation unit;
  ticks were not counted as independent samples.
- The confidence intervals in the tables are seed-level, 10,000-draw bootstrap 95%
  **marginal** intervals. No p-value or familywise correction was applied;
  interpretations rest on effect sizes and their intervals.

## Primary results

Last-100-tick mean per cell; the square brackets are the 95% bootstrap CI, `SD`
is the between-seed standard deviation.

| Capacity / regen | Cooperation measure | Conflict measure | True scarcity |
|---|---:|---:|---:|
| 90 / 0.016 | 0.174 [0.172, 0.177], SD 0.007 | 0.320 [0.316, 0.324], SD 0.011 | 0.978 [0.963, 0.992], SD 0.042 |
| 90 / 0.019 | 0.206 [0.199, 0.214], SD 0.022 | 0.287 [0.278, 0.295], SD 0.026 | 0.803 [0.744, 0.860], SD 0.165 |
| 120 / 0.016 | 0.252 [0.244, 0.261], SD 0.024 | 0.231 [0.222, 0.241], SD 0.027 | 0.493 [0.431, 0.555], SD 0.178 |
| 120 / 0.019 | 0.308 [0.300, 0.315], SD 0.022 | 0.178 [0.171, 0.184], SD 0.018 | 0.169 [0.123, 0.221], SD 0.140 |

### Factorial contrasts

Effect = high level minus low level. Interaction = the difference of the capacity
differences between the regeneration levels.

| Outcome | Capacity effect | Regeneration effect | Capacity × regeneration |
|---|---:|---:|---:|
| Cooperation measure | +0.090 [0.083, 0.097] | +0.044 [0.036, 0.051] | +0.023 [0.009, 0.037] |
| Conflict measure | −0.099 [−0.107, −0.091] | −0.043 [−0.051, −0.036] | −0.020 [−0.035, −0.005] |
| True scarcity | −0.560 [−0.610, −0.510] | −0.249 [−0.299, −0.199] | −0.149 [−0.249, −0.046] |

For cooperation and conflict, all the contrast intervals lay in the direction
expected within the model: under high capacity/regeneration conditions the share of
`share`/`socialize` actions rose and the `steal` share fell. The resource
manipulation also produced a clear change in the scarcity measure. This is the
within-simulation effect of the manipulated configurations; it does not by itself
show that scarcity causes these outcomes in human societies.

## Seed variability and second-level findings

Although the mean scarcity of the `120 / 0.016` condition is in the middle band, the
seeds did not follow a similar course: the last-window seed mean stayed in the range
0.30–0.60 in 17/30 seeds; the range was 0.085–0.819. Therefore "middle mean" does not
mean that every run stayed at medium scarcity. The variability of the scarcity
trajectories is an important research topic.

Other last-window means:

| Capacity / regen | Stress | Mean trust | Gini | Population |
|---|---:|---:|---:|---:|
| 90 / 0.016 | 0.842 | −0.034 | 0.412 | 93.1 |
| 90 / 0.019 | 0.763 | −0.015 | 0.403 | 105.0 |
| 120 / 0.016 | 0.653 | 0.002 | 0.415 | 111.5 |
| 120 / 0.019 | 0.518 | 0.016 | 0.427 | 117.3 |

While stress and trust changed in the expected direction under more favorable
resource conditions, Gini did not fall; it came out slightly higher at the high
capacity level. This is an exploratory finding showing that, in the model, resource
abundance does not automatically reduce inequality. The seed intervals and mechanism
interactions for Gini should be examined separately.

## Measure definitions and limits

- `cooperation_rate` is the share of living agents whose final action is `share`
  **or** `socialize`. It is a narrow proxy measure of cooperative behavior.
- `conflict_rate` is the share of living agents whose final action is `steal`;
  it is not a measure of physical violence.
- `true_scarcity` is derived from the ratio of the physical food/water stocks to
  capacity. Agents' beliefs are not the same thing as this true value.
- Agents are processed within a tick in a fixed list order and with immediate
  effects. Follow-up comparisons with shuffled order and per-agent RNG were made
  afterwards: `SCHEDULE_ROBUSTNESS_RESULTS.md`, `AGENT_RNG_ROBUSTNESS_RESULTS.md`.
- The cooperation/conflict contrasts depend on the direct `scarcity_belief` terms in
  the decision formula (ISSUE-013); the decomposition is in
  `SCARCITY_LINK_ABLATION_RESULTS.md`.
- The experiment manipulated resource parameters; it did not assign scarcity as a
  separately isolated intervention. A new experimental design is needed for
  mediator claims.
- Seed-based bootstrap intervals summarize seed uncertainty; they do not cover
  uncertainty in the model structure, the chosen mechanism and the parameter
  assumptions.

## Reproduction files

- [Full results JSON](output/resource_factorial/results.json): configuration,
  seed assignment, cell statistics and all factorial contrasts.
- [Seed summaries CSV](output/resource_factorial/seed_summaries.csv): last-100-tick
  means for each of the 120 seeds.
- [Full time series CSV](output/resource_factorial/timeseries.csv): all ticks and
  metrics of every seed (60,000 rows).
- Code and the method written in advance: `run_resource_factorial.py`,
  `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md`.
