# Protocol: Real Deprivation × Decision Architecture

**Status:** the protocol was written before the run (2026-10-09). The results are
reported in the separate file `DEPRIVATION_RESULTS.md`.

## Question

The earlier resource experiments were run in regimes where the agents were well fed;
what was measured was the response to the belief about the stores indicator
(ISSUE-015). When the stores indicator is held fixed (empty) and the agents are
really deprived, do the conflict and cooperation measures change, and does this
change depend on the decision architecture?

## Pilot and regime selection

`run_deprivation_pilot.py` swept capacity 90/120 × nine regeneration levels × 4
seeds. The selection rule was written into the script before the run: the highest
regeneration level at which the last-window `need_deficit_rate` mean is ≥ 0.20 at
both capacities and the population fell below 20 in none of the pilot seeds. The
rule looks only at need and population; it does not look at cooperation/conflict
results.

- **Fixed agent order (default), seeds 91000–91071:** no level passed the rule.
  Scarcity produces starvation death rather than persistent deprivation; the
  survivors stay well fed (in the last window the deprived share is 2–8%). The cause
  is ISSUE-016: in fixed order, agents with low IDs reach the stores first.
- **Shuffled order, seeds 93000–93071:** 0.003 and 0.004 passed the rule;
  **the selected level is 0.004** (the deprived share is 0.25 at capacity 90 and
  0.27 at 120).

For the comparison level, a second rule was written after the pilot was seen and
looks only at the stores indicator: the highest regeneration level at which the mean
`true_scarcity` is ≥ 0.99 at both capacities. This is **0.010** (deprived share 0.06
and 0.03). Thus at both levels the stores look empty; the difference lies in
deprivation. The cooperation/conflict measures were not looked at in the pilot.

In addition, to see whether the summary code would break if the population were
wiped out, the `scoring_only` and `need_based` arms were run with two seeds
(92010–92011) in the selected deprivation cell and **only the population** was
looked at (38–85; no extinction).

## Design

- Capacity 90/120; food and water regeneration together **0.004 (deprived) /
  0.010 (empty stores, well fed)**; initial stock 2/3 of capacity.
- On the decision side a 2×2, four arms: `intact`, `provisions_only`, `scoring_only`,
  `need_based` (definitions in `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`).
- **`agent_update_order="shuffled"`.** In this regime the fixed order produces
  priority by agent ID (ISSUE-016) and does not create persistent deprivation; this
  experiment does not use it. The results should not be compared directly with the
  earlier (fixed-order) experiments.
- 2×2×4 = 16 cells; 30 seed blocks (94000–94029) in each cell; 480 simulations.
  The seed range had not been used before.
- 80 founder agents, 500 ticks, `agent_rng_mode="shared"`. The last 100 ticks are
  averaged within each seed; the seed is the unit of analysis. The `provision_*`
  values do not change.

## Measures and analysis

**Manipulation check:** the regeneration contrast (high minus low = well fed minus
deprived) of `need_deficit_rate` and `avg_min_need` must exclude zero in every arm;
`true_scarcity` must be ≈ 1 in every cell. If the deprivation contrast of an arm
covers zero, the primary contrasts of that arm are not interpreted.

**Primary:** the main effect of regeneration (well fed minus deprived) for
`conflict_rate` and `cooperation_rate`, in each arm; and the provisions × scoring
decomposition of this contrast.

**Secondary (exploratory):** action shares, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `cumulative_deaths_starvation`,
identity label shares; capacity contrasts.

Uncertainty: 10,000-draw seed-block bootstrap, 95% percentile interval.
No p-value or multiple-comparison correction; all cells are reported.

## Expectations written in advance

Since belief is saturated (≈1) at both levels, the direct `scarcity_belief` terms
should not produce a difference between the two levels; the differences come from the
need, stress and death channels.

- **`intact` and `provisions_only`:** there is no need term in the `steal` score.
  Under deprivation the `forage` score rises and squeezes out the other actions.
  Expectation: in the deprived condition the `steal` share is **lower** (conflict
  contrast positive), and the cooperation share is also lower (cooperation contrast
  positive).
- **`scoring_only` and `need_based`:** the `steal` score rises with urgency, `share`
  falls; the urgency term in the `forage` score is almost nullified by the saturated
  belief (since the agent thinks the stores are empty it does not turn to foraging).
  Expectation: in the deprived condition the `steal` share is **higher** (conflict
  contrast negative), cooperation is lower (contrast positive). Because foraging
  falls in these arms, deprivation and starvation death may be greater than in
  `intact`.
- **Provisions:** since agents now fall below the threshold, eating is triggered.
  Expectation: provisions lower the deprived share; the effect on the primary
  contrasts is small but larger than in the earlier experiment.

## Interpretation rules

- If the conflict contrast has opposite signs in the two architecture groups and the
  intervals exclude zero: the **direction** of the effect of real deprivation on
  conflict depends on the decision-rule assumption.
- If the interval covers zero in an arm: there is no distinguishable effect in this
  sample.
- A result that disagrees with the expectations is reported as it is; the score terms
  or `provision_*` values are not changed by looking at the result (principle 9).

## Limits

- Deprivation is persistent but the population also falls; the population differs
  between cells, and the rates are computed over populations of different sizes.
- The comparison level (0.010) is not fully well fed (deprived share 0.03–0.06).
- The second selection rule was written after the pilot was seen.
- Shuffled order is also a timing assumption; simultaneous updating was not tested.
  Mass conservation in foraging is not exact; there is no calibration with external
  data.

## Implementation

```
py run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based \
   --capacities 90,120 --regen-rates 0.004,0.010 --order shuffled --seed-start 94000 \
   --out-dir output/deprivation --protocol EXPERIMENT_PROTOCOL_DEPRIVATION.md
py analyze_scarcity_link_ablation.py --dir output/deprivation \
   --factorial provisions_only,scoring_only,need_based
```
