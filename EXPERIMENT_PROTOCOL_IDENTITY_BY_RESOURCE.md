# Protocol: Resource Regime × Identity Feedback

## Question

Does raising `identity_feedback_strength` change trust and conflict; does this effect
differ by capacity/regeneration regime?

## Rationale and limit of the claim

In the earlier V6 re-test (`REVALIDATION.md`), the identity feedback 0.0→0.5
comparison in the default resource regime was associated with `avg_trust`,
`conflict_rate`, `inequality_gini` and population. The monotonic dose claim in the
old mechanism sweep rested on only five seeds. This follow-up carries the selected
extreme contrast to the previously examined 2×2 resource range. It is a
theoretical/exploratory, within-model experiment; it does not aim at external
validity or at causal claims about human behavior.

## Design determined in advance

- Factors: resource capacity 90/120; food and water regeneration rate 0.016/0.019;
  `identity_feedback_strength` 0.0/0.5.
- 2×2×2 = 8 cells; 30 seeds per cell; 240 simulations in total.
- Each seed is used in all eight conditions (seed-blocked/matched design); seeds
  50000–50029. The same seed label is not a full common-random-numbers guarantee:
  when the mechanism differs, the shared RNG draws may shift to different branches.
- Each world has 80 founder agents and 500 ticks; food/water start is 2/3 of capacity.
- The update order is fixed; `agent_rng_mode="shared"` preserves the current default
  and provides comparability with the old V6 results. The RNG and order
  uncertainties are recorded as limitations of this design.
- Unit: one seed/condition simulation. Metrics are averaged per seed within the last
  100 ticks. Ticks are not counted as independent samples.

## Outcome measures and analysis

The primary measures are `avg_trust`, `conflict_rate` and `cooperation_rate`, which
is a narrow behavioral proxy. The primary estimates are the matched seed difference
of identity feedback 0.5 minus 0.0 in each resource cell; plus the identity×capacity,
identity×regen and triple-interaction contrasts, which show whether the resource
factors change the identity effect. 95% seed-block bootstrap intervals are produced
with 10,000 draws and a recorded analysis seed. Estimates and intervals are reported
instead of p-values; to avoid selectively highlighting results, all cells and primary
contrasts are shown.

The secondary measures are `true_scarcity`, `inequality_gini`, `population`,
`identity_formed_rate` and `positive_relationship_rate`; they are labeled
exploratory. Since no calibration/validation with external data is done, all
interpretations are limited to the current model mechanisms.

## Stopping and reporting

30 seeds/cell is the pre-specified pilot/final sample; it is not a guarantee of
adequacy. After the runs start, the sample/measures are not changed by looking at the
results. The outputs are written into `output/identity_resource_factorial/` with seed
summaries, the full time series and the configuration.
