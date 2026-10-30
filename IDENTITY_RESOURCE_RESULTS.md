# Identity Feedback × Resource Regime — Results

## Status and scope

**Experiment completed: 2026-10-05.** This is a 2×2×2 factorial, within-model
exploratory analysis; it is not a calibration to human data or an empirical validation.

## Method

- 80 founder agents, 500 ticks; the last 100 ticks were averaged within each seed.
- Resource capacity 90/120; food and water regeneration together 0.016/0.019.
- `identity_feedback_strength` 0.0/0.5. The initial food/water stock was 2/3 of
  capacity in all conditions.
- 8 condition cells × 30 seeds = 240 simulations. The same 30 seeds were used in all
  eight cells (50000–50029), so seed blocking was applied.
- Fixed agent order and the current default `agent_rng_mode="shared"` were used.
  As intervention paths diverge, the same seed label does not preserve the alignment
  of RNG draws; the pairing is not a full common-random-numbers design.
- The seed simulation is the unit of analysis. 10,000 paired seed-block bootstrap
  resamples were used. No binary decision by p-value and no multiple-measure
  correction was made.

## Primary results

Identity effect = `identity_feedback_strength=0.5` minus `0.0`. Brackets are
95% seed-bootstrap intervals. Cooperation is a narrow proxy measure; it is the share
of `share` or `socialize` as the final action. Conflict is the share of `steal` as
the final action.

| Resource regime | Mean trust | Conflict measure | Cooperation measure |
|---|---:|---:|---:|
| 90 / 0.016 | −0.0182 [−0.0198, −0.0168] | +0.0579 [+0.0522, +0.0636] | −0.0314 [−0.0357, −0.0275] |
| 90 / 0.019 | −0.0165 [−0.0194, −0.0136] | +0.0430 [+0.0359, +0.0501] | −0.0192 [−0.0267, −0.0115] |
| 120 / 0.016 | −0.0138 [−0.0162, −0.0112] | +0.0273 [+0.0165, +0.0387] | −0.0102 [−0.0229, +0.0019] |
| 120 / 0.019 | −0.0126 [−0.0146, −0.0106] | +0.0175 [+0.0095, +0.0257] | +0.0014 [−0.0077, +0.0100] |

## Identity × resource contrasts

The contrasts are the difference of the 0.5–0.0 effect of identity feedback between
the high resource factor and the low resource factor. The triple term is the
difference in how the capacity-dependent identity effect changes with the
regeneration level.

| Outcome | Identity mean effect | Identity × capacity | Identity × regeneration | Triple interaction |
|---|---:|---:|---:|---:|
| Mean trust | −0.0152 [−0.0163, −0.0142] | +0.0042 [+0.0017, +0.0067] | +0.0015 [−0.0010, +0.0039] | −0.0006 [−0.0045, +0.0034] |
| Conflict measure | +0.0364 [+0.0318, +0.0409] | −0.0280 [−0.0373, −0.0181] | −0.0123 [−0.0202, −0.0047] | +0.0050 [−0.0063, +0.0173] |
| Cooperation measure | −0.0149 [−0.0195, −0.0101] | +0.0209 [+0.0105, +0.0304] | +0.0119 [+0.0036, +0.0210] | −0.0006 [−0.0144, +0.0122] |

The results support that, in this model, high identity feedback lowers trust and
raises the `steal` share. This relationship came out larger at low capacity. The
decline in the cooperation measure was pronounced in the low-capacity conditions; in
high capacity/high regeneration the interval covered zero. Regeneration's reduction
of the identity effect is seen in the conflict and cooperation measures, whereas for
trust the interval covers zero. The triple-interaction intervals covered zero.

## Secondary exploratory results

The mean of the identity effect across the four resource cells:

| Measure | Identity effect (95% CI) |
|---|---:|
| True scarcity | −0.0110 [−0.0421, +0.0193] |
| Gini inequality | +0.1106 [+0.1055, +0.1155] |
| Final population | −10.51 [−12.35, −8.63] |
| Identity formation rate | +0.0023 [+0.0014, +0.0033] |
| Positive relationship rate | −0.0360 [−0.0397, −0.0323] |

Gini, population and the other secondary measures were marked as exploratory in the
protocol; no multiple-comparison correction was applied. Even though the Gini
difference in particular looks large, the mechanism needs to be decomposed and the
analysis repeated under alternative structural assumptions. Identity feedback does
not appear to have changed the resource scarcity measure noticeably; the scarcity
level is an outcome in this experiment, not a mediating variable that was
experimentally fixed.

## Interpretation limits and next step

- The `identity_feedback_strength` endpoints 0.0/0.5 were tested; the dose-response
  curve was not re-examined in these new regimes.
- Seed bootstrap summarizes uncertainty; it does not include uncertainty about the
  mechanism, parameters and measurement definition.
- The identity formation rate may be high; a mean identity effect does not mean that
  all identity labels or behavioral pathways are explained separately.
- The next step is first to examine seed-level trajectories and identity labels in
  order to decompose the Gini/population effect; then to test intermediate doses in
  the resource regimes only with a pre-specified hypothesis.

## Addendum (2026-10-07): label and action shares — post hoc, exploratory

The first run had not recorded the identity label shares and the separate shares of
actions. `run_identity_label_followup.py` re-ran the same 240 worlds with the same
seeds; in all 240 runs `mean_conflict_rate` matched the original seed summaries
(difference ≤ 1e−12). This analysis was not in the protocol; the results were added
after being seen and contain no interval/multiple-comparison correction. The values
are the 30-seed mean of the last 100 ticks; the arrow is `identity_feedback_strength`
0.0 → 0.5.

| Resource regime | `benefactor` share | `opportunist` share | `survivor` share | `steal` share | `share` share | Gini |
|---|---:|---:|---:|---:|---:|---:|
| 90 / 0.016 | 0.078 → 0.063 | 0.523 → 0.488 | 0.394 → 0.445 | 0.285 → 0.343 | 0.093 → 0.074 | 0.351 → 0.462 |
| 90 / 0.019 | 0.264 → 0.217 | 0.409 → 0.422 | 0.314 → 0.353 | 0.267 → 0.310 | 0.105 → 0.098 | 0.347 → 0.451 |
| 120 / 0.016 | 0.439 → 0.339 | 0.305 → 0.387 | 0.240 → 0.262 | 0.217 → 0.244 | 0.140 → 0.142 | 0.351 → 0.465 |
| 120 / 0.019 | 0.526 → 0.406 | 0.250 → 0.357 | 0.206 → 0.220 | 0.171 → 0.189 | 0.176 → 0.189 | 0.362 → 0.475 |

Observations:

- **Label composition depends on the resource regime.** Even with feedback off, the
  `opportunist` share is 0.52 in the scarcest regime and 0.25 in the most abundant
  regime; the `benefactor` share is 0.08 versus 0.53. The "identity effect" is
  applied to a different label mix in each regime.
- **Where the `steal` increase is largest, the `opportunist` share does not
  increase.** At 90/0.016, `steal` rises by +0.058 while the `opportunist` share
  falls from 0.523 to 0.488 (increase in 5 of 30 seeds). The increase here appears
  to come not from label conversion but from the direct bonus (`decision.py`) added
  to the `steal` score of `opportunist` agents, who are already half the population.
  That is, the conflict effect that comes out larger at low capacity is largely
  consistent with "initial `opportunist` share × fixed bonus" (ISSUE-013).
- **At high capacity the mechanism is different.** The `benefactor` share falls by
  0.10–0.12 and the `opportunist` share rises by 0.08–0.11 (in 28–29 of 30 seeds);
  despite this, the `share` share does not fall, it rises slightly. Feedback changes
  the label composition here, but the bonus of the remaining `benefactor` agents
  preserves the `share` share.
- **The Gini increase is independent of regime.** It lies between +0.104 and +0.114
  in the four cells and is positive in all 120 seed pairs. While the `steal` increase
  varies threefold across regimes, the Gini increase does not vary; therefore the Gini
  difference cannot be explained by the stealing rate alone. Candidate explanations
  (untested): the `survivor` label's `forage` bonus may be concentrating the sole
  income source in particular agents; the `forage` share rises in all four cells.
  This requires wealth recording by label.
- The `socialize` and `spread_belief` shares fall in all four cells; the decline in
  the cooperation measure appears to stem from `share` + `socialize` at low capacity
  and from `socialize` alone at high capacity.

Files: `output/identity_label_followup/seed_summaries.csv`, `summary.json`.

## Reproduction files

- Protocol: `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`.
- Run script: `run_identity_resource_factorial.py`.
- Analysis: `analyze_identity_resource_factorial.py`.
- Design metadata and analysis JSON: `output/identity_resource_factorial/experiment.json`, `analysis.json`.
- Seed summaries: `output/identity_resource_factorial/seed_summaries.csv` (240 rows).
- Full time series: `output/identity_resource_factorial/timeseries.csv` (120,000 tick rows).
